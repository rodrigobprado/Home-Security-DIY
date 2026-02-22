#pragma once

struct PidState {
    float kp;
    float ki;
    float kd;
    float integral;
    float previousError;
    bool initialized;
};

float clampf(float value, float minValue, float maxValue);
int clamp_pwm(int value);
float compute_pid(PidState& state, float setpoint, float measurement, float dtSeconds);
