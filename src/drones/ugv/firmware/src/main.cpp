#include <Arduino.h>
#include <LoRa.h>
#include <SPI.h>

#include "motor_control.h"

// =============================================================================
// PIN DEFINITIONS
// =============================================================================
// Motor driver pins (BTS7960 / IBT-2)
// NOTE: GPIO 18/19 intentionally unused to avoid historical conflict with SPI/LoRa (issue #30).
#define RPWM_L 16
#define LPWM_L 17
#define RPWM_R 25
#define LPWM_R 26

// Encoder pins
#define ENC_L_A 34
#define ENC_L_B 35
#define ENC_R_A 32
#define ENC_R_B 33
#define BATTERY_ADC_PIN 39

// LoRa SX1276 (HSPI)
#define LORA_SS 5
#define LORA_RST 27
#define LORA_DIO0 2
#define LORA_SCK 14
#define LORA_MISO 12
#define LORA_MOSI 13

// PWM channels (ESP32 LEDC)
#define CH_RPWM_L 0
#define CH_LPWM_L 1
#define CH_RPWM_R 2
#define CH_LPWM_R 3
#define PWM_FREQ 20000
#define PWM_RES_BITS 8

// =============================================================================
// GLOBALS
// =============================================================================
volatile long encoderLeftPos = 0;
volatile long encoderRightPos = 0;

unsigned long lastStatusTime = 0;
const unsigned long STATUS_INTERVAL_MS = 100; // 10Hz telemetry

unsigned long lastControlTime = 0;
const unsigned long CONTROL_INTERVAL_MS = 50; // 20Hz PID control

unsigned long lastCmdTime = 0;
const unsigned long COMMAND_TIMEOUT_MS = 800; // watchdog

unsigned long lastLoraHeartbeat = 0;
const unsigned long LORA_INTERVAL_MS = 5000;

long lastEncoderLeft = 0;
long lastEncoderRight = 0;

int targetLeftPwm = 0;
int targetRightPwm = 0;
int appliedLeftPwm = 0;
int appliedRightPwm = 0;

const float MAX_TICKS_PER_SECOND = 1800.0f;

PidState pidLeft{0.15f, 0.02f, 0.01f, 0.0f, 0.0f, false};
PidState pidRight{0.15f, 0.02f, 0.01f, 0.0f, 0.0f, false};

// =============================================================================
// INTERRUPTS
// =============================================================================
void IRAM_ATTR isr_enc_l() {
  if (digitalRead(ENC_L_B) == HIGH) {
    encoderLeftPos++;
  } else {
    encoderLeftPos--;
  }
}

void IRAM_ATTR isr_enc_r() {
  if (digitalRead(ENC_R_B) == HIGH) {
    encoderRightPos++;
  } else {
    encoderRightPos--;
  }
}

// =============================================================================
// MOTOR CONTROL
// =============================================================================
void setupPwm() {
  ledcSetup(CH_RPWM_L, PWM_FREQ, PWM_RES_BITS);
  ledcSetup(CH_LPWM_L, PWM_FREQ, PWM_RES_BITS);
  ledcSetup(CH_RPWM_R, PWM_FREQ, PWM_RES_BITS);
  ledcSetup(CH_LPWM_R, PWM_FREQ, PWM_RES_BITS);

  ledcAttachPin(RPWM_L, CH_RPWM_L);
  ledcAttachPin(LPWM_L, CH_LPWM_L);
  ledcAttachPin(RPWM_R, CH_RPWM_R);
  ledcAttachPin(LPWM_R, CH_LPWM_R);
}

void setMotorSpeed(int pwmChannelFwd, int pwmChannelRev, int speed) {
  const int pwm = clamp_pwm(speed);
  if (pwm > 0) {
    ledcWrite(pwmChannelFwd, pwm);
    ledcWrite(pwmChannelRev, 0);
  } else if (pwm < 0) {
    ledcWrite(pwmChannelFwd, 0);
    ledcWrite(pwmChannelRev, -pwm);
  } else {
    ledcWrite(pwmChannelFwd, 0);
    ledcWrite(pwmChannelRev, 0);
  }
}

void stopMotors() {
  targetLeftPwm = 0;
  targetRightPwm = 0;
  appliedLeftPwm = 0;
  appliedRightPwm = 0;
  setMotorSpeed(CH_RPWM_L, CH_LPWM_L, 0);
  setMotorSpeed(CH_RPWM_R, CH_LPWM_R, 0);
}

// =============================================================================
// SERIAL PROTOCOL
// =============================================================================
// RX frames:
//   M <left_pwm> <right_pwm>   (range -255..255)
//   STOP                       (immediate motor stop)
// TX frames:
//   O <left_ticks> <right_ticks>
//   B <battery_percent>
//   W <watchdog_ok 0|1>

void processSerialCommand(const String &inputRaw) {
  String input = inputRaw;
  input.trim();
  if (input.length() == 0) {
    return;
  }

  if (input == "STOP") {
    stopMotors();
    return;
  }

  if (input.startsWith("M ")) {
    int firstSpace = input.indexOf(' ');
    int secondSpace = input.lastIndexOf(' ');
    if (firstSpace > -1 && secondSpace > firstSpace) {
      int left = input.substring(firstSpace + 1, secondSpace).toInt();
      int right = input.substring(secondSpace + 1).toInt();

      targetLeftPwm = clamp_pwm(left);
      targetRightPwm = clamp_pwm(right);
      lastCmdTime = millis();
    }
  }
}

// =============================================================================
// BATTERY
// =============================================================================
int readBatteryPercent() {
  static float filtered = 0.0f;
  const int raw = analogRead(BATTERY_ADC_PIN);

  if (filtered == 0.0f) {
    filtered = raw;
  }
  filtered = (0.85f * filtered) + (0.15f * raw);

  // Calibration window for ADC -> battery %. Must be adjusted per hardware divider.
  const int adcMin = 1700;
  const int adcMax = 3200;
  int percent = map((int)filtered, adcMin, adcMax, 0, 100);
  percent = constrain(percent, 0, 100);
  return percent;
}

// =============================================================================
// PID LOOP
// =============================================================================
void controlLoop() {
  const unsigned long now = millis();
  if (now - lastControlTime < CONTROL_INTERVAL_MS) {
    return;
  }

  const float dt = (now - lastControlTime) / 1000.0f;
  lastControlTime = now;

  const long encL = encoderLeftPos;
  const long encR = encoderRightPos;

  const float measuredL = (encL - lastEncoderLeft) / dt;
  const float measuredR = (encR - lastEncoderRight) / dt;

  lastEncoderLeft = encL;
  lastEncoderRight = encR;

  const float targetL = (targetLeftPwm / 255.0f) * MAX_TICKS_PER_SECOND;
  const float targetR = (targetRightPwm / 255.0f) * MAX_TICKS_PER_SECOND;

  const float correctionL = compute_pid(pidLeft, targetL, measuredL, dt);
  const float correctionR = compute_pid(pidRight, targetR, measuredR, dt);

  appliedLeftPwm = clamp_pwm((int)(targetLeftPwm + correctionL));
  appliedRightPwm = clamp_pwm((int)(targetRightPwm + correctionR));

  setMotorSpeed(CH_RPWM_L, CH_LPWM_L, appliedLeftPwm);
  setMotorSpeed(CH_RPWM_R, CH_LPWM_R, appliedRightPwm);
}

void setup() {
  Serial.begin(115200);

  pinMode(ENC_L_A, INPUT);
  pinMode(ENC_L_B, INPUT);
  pinMode(ENC_R_A, INPUT);
  pinMode(ENC_R_B, INPUT);
  pinMode(BATTERY_ADC_PIN, INPUT);

  setupPwm();

  attachInterrupt(digitalPinToInterrupt(ENC_L_A), isr_enc_l, RISING);
  attachInterrupt(digitalPinToInterrupt(ENC_R_A), isr_enc_r, RISING);

  Serial.println("Starting LoRa...");
  SPI.begin(LORA_SCK, LORA_MISO, LORA_MOSI, LORA_SS);
  LoRa.setPins(LORA_SS, LORA_RST, LORA_DIO0);
  if (!LoRa.begin(915E6)) {
    Serial.println("Starting LoRa failed!");
  } else {
    Serial.println("LoRa Started");
  }

  lastCmdTime = millis();
  lastControlTime = millis();
  Serial.println("UGV Firmware v0.3 Ready");
}

void loop() {
  // 1) Read serial commands
  if (Serial.available() > 0) {
    processSerialCommand(Serial.readStringUntil('\n'));
  }

  // 2) Watchdog: fail-safe stop on command timeout
  const bool watchdogOk = (millis() - lastCmdTime) <= COMMAND_TIMEOUT_MS;
  if (!watchdogOk && (targetLeftPwm != 0 || targetRightPwm != 0)) {
    stopMotors();
  }

  // 3) Backup LoRa commands
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    String loraInput = "";
    while (LoRa.available()) {
      loraInput += (char)LoRa.read();
    }
    Serial.print("LoRa Recv: ");
    Serial.println(loraInput);

    if (loraInput == "CMD:STOP") {
      stopMotors();
      Serial.println("EMERGENCY STOP VIA LORA");
    }
  }

  // 4) PID control loop
  controlLoop();

  // 5) Telemetry frames
  if (millis() - lastStatusTime >= STATUS_INTERVAL_MS) {
    lastStatusTime = millis();
    Serial.printf("O %ld %ld\n", encoderLeftPos, encoderRightPos);
    Serial.printf("B %d\n", readBatteryPercent());
    Serial.printf("W %d\n", watchdogOk ? 1 : 0);
  }

  // 6) LoRa heartbeat
  if (millis() - lastLoraHeartbeat >= LORA_INTERVAL_MS) {
    lastLoraHeartbeat = millis();
    LoRa.beginPacket();
    LoRa.print("UGV:ALIVE:BAT=OK");
    LoRa.endPacket();
  }
}
