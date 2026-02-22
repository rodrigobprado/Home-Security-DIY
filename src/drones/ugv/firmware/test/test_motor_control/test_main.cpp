#include <unity.h>
#include "motor_control.h"

void test_clamp_pwm_limits() {
    TEST_ASSERT_EQUAL(255, clamp_pwm(300));
    TEST_ASSERT_EQUAL(-255, clamp_pwm(-300));
    TEST_ASSERT_EQUAL(42, clamp_pwm(42));
}

void test_pid_positive_error_generates_positive_output() {
    PidState state{0.5f, 0.1f, 0.0f, 0.0f, 0.0f, false};
    const float out = compute_pid(state, 100.0f, 0.0f, 0.05f);
    TEST_ASSERT_TRUE(out > 0.0f);
}

void test_pid_negative_error_generates_negative_output() {
    PidState state{0.5f, 0.1f, 0.0f, 0.0f, 0.0f, false};
    const float out = compute_pid(state, -100.0f, 0.0f, 0.05f);
    TEST_ASSERT_TRUE(out < 0.0f);
}

int main() {
    UNITY_BEGIN();
    RUN_TEST(test_clamp_pwm_limits);
    RUN_TEST(test_pid_positive_error_generates_positive_output);
    RUN_TEST(test_pid_negative_error_generates_negative_output);
    return UNITY_END();
}
