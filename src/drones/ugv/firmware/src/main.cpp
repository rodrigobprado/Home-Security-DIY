#include <Arduino.h>
#include <LoRa.h>

// =============================================================================
// PIN DEFINITIONS
// =============================================================================
// Driver Motor (BTS7960 / IBT-2)
#define RPWM_L 16  // Right PWM Left Motor
#define LPWM_L 17  // Left PWM Left Motor
#define RPWM_R 18  // Right PWM Right Motor
#define LPWM_R 19  // Left PWM Right Motor

// Encoders (Interrupt pins)
#define ENC_L_A 34
#define ENC_L_B 35
#define ENC_R_A 32
#define ENC_R_B 33

// LoRa SX1276 (SPI)
#define LORA_SS 5
#define LORA_RST 14
#define LORA_DIO0 2
#define LORA_SCK 18  // SPI SCK (Check your board)
#define LORA_MISO 19 // SPI MISO
#define LORA_MOSI 23 // SPI MOSI

// =============================================================================
// GLOBALS
// =============================================================================
volatile long encoderLeftPos = 0;
volatile long encoderRightPos = 0;

unsigned long lastStatusTime = 0;
const int STATUS_INTERVAL = 100; // 10Hz serial odometry update

unsigned long lastLoraHeartbeat = 0;
const int LORA_INTERVAL = 5000;  // 5s LoRa heartbeat

// =============================================================================
// INTERRUPT SERVICE ROUTINES
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
void setMotorSpeed(int pinFwd, int pinRev, int speed) {
    if (speed > 0) {
        analogWrite(pinFwd, speed);
        analogWrite(pinRev, 0);
    } else if (speed < 0) {
        analogWrite(pinFwd, 0);
        analogWrite(pinRev, -speed);
    } else {
        analogWrite(pinFwd, 0);
        analogWrite(pinRev, 0);
    }
}

void setup() {
    Serial.begin(115200);

    // Motor Pins
    pinMode(RPWM_L, OUTPUT);
    pinMode(LPWM_L, OUTPUT);
    pinMode(RPWM_R, OUTPUT);
    pinMode(LPWM_R, OUTPUT);

    // Encoder Pins
    pinMode(ENC_L_A, INPUT);
    pinMode(ENC_L_B, INPUT);
    pinMode(ENC_R_A, INPUT);
    pinMode(ENC_R_B, INPUT);

    // Interrupts
    attachInterrupt(digitalPinToInterrupt(ENC_L_A), isr_enc_l, RISING);
    attachInterrupt(digitalPinToInterrupt(ENC_R_A), isr_enc_r, RISING);

    // LoRa Setup
    Serial.println("Starting LoRa...");
    LoRa.setPins(LORA_SS, LORA_RST, LORA_DIO0);
    if (!LoRa.begin(915E6)) { // 915MHz for Americas (Check local regulations)
        Serial.println("Starting LoRa failed!");
    } else {
        Serial.println("LoRa Started");
    }

    Serial.println("UGV Firmware v0.2 Ready");
}

void loop() {
    // -------------------------------------------------------------------------
    // 1. READ SERIAL COMMANDS (Primary - High Bandwidth)
    // Format: "M <left_pwm> <right_pwm>"
    // -------------------------------------------------------------------------
    if (Serial.available() > 0) {
        String input = Serial.readStringUntil('\n');
        input.trim();

        if (input.startsWith("M ")) {
            int firstSpace = input.indexOf(' ');
            int secondSpace = input.lastIndexOf(' '); // Assuming only 2 spaces

            if (firstSpace != -1) {
                 // Simple parsing logic... optimized for robust serial
                 // For now, let's keep it simple
                 int leftSpeed = 0;
                 int rightSpeed = 0;
                 
                 // sscanf is safer if available, but String is easy
                 if(secondSpace > firstSpace) {
                     leftSpeed = input.substring(firstSpace + 1, secondSpace).toInt();
                     rightSpeed = input.substring(secondSpace + 1).toInt();
                 }

                leftSpeed = constrain(leftSpeed, -255, 255);
                rightSpeed = constrain(rightSpeed, -255, 255);

                setMotorSpeed(RPWM_L, LPWM_L, leftSpeed);
                setMotorSpeed(RPWM_R, LPWM_R, rightSpeed);
            }
        }
    }

    // -------------------------------------------------------------------------
    // 2. READ LORA COMMANDS (Backup - Low Bandwidth)
    // Format: "CMD:STOP" or "CMD:HOME"
    // -------------------------------------------------------------------------
    int packetSize = LoRa.parsePacket();
    if (packetSize) {
        String loraInput = "";
        while (LoRa.available()) {
            loraInput += (char)LoRa.read();
        }
        Serial.print("LoRa Recv: ");
        Serial.println(loraInput);
        
        if(loraInput == "CMD:STOP") {
            setMotorSpeed(RPWM_L, LPWM_L, 0);
            setMotorSpeed(RPWM_R, LPWM_R, 0);
            Serial.println("EMERGENCY STOP VIA LORA");
        }
    }

    // -------------------------------------------------------------------------
    // 3. SEND ODOMETRY (Serial - Fast)
    // -------------------------------------------------------------------------
    if (millis() - lastStatusTime >= STATUS_INTERVAL) {
        lastStatusTime = millis();
        Serial.printf("O %ld %ld\n", encoderLeftPos, encoderRightPos);
    }

    // -------------------------------------------------------------------------
    // 4. SEND LORA HEARTBEAT (Backup - Slow)
    // -------------------------------------------------------------------------
    if (millis() - lastLoraHeartbeat >= LORA_INTERVAL) {
        lastLoraHeartbeat = millis();
        LoRa.beginPacket();
        LoRa.print("UGV:ALIVE:BAT=OK");
        LoRa.endPacket();
    }
}
