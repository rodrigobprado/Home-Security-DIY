#include "motor_control.h"

float clampf(float value, float minValue, float maxValue) {
    if (value < minValue) return minValue;
    if (value > maxValue) return maxValue;
    return value;
}

int clamp_pwm(int value) {
    if (value > 255) return 255;
    if (value < -255) return -255;
    return value;
}

float compute_pid(PidState& state, float setpoint, float measurement, float dtSeconds) {
    if (dtSeconds <= 0.0f) {
        return 0.0f;
    }

    const float error = setpoint - measurement;
    state.integral += error * dtSeconds;
    state.integral = clampf(state.integral, -500.0f, 500.0f);

    float derivative = 0.0f;
    if (state.initialized) {
        derivative = (error - state.previousError) / dtSeconds;
    } else {
        state.initialized = true;
    }

    state.previousError = error;
    return (state.kp * error) + (state.ki * state.integral) + (state.kd * derivative);
}
