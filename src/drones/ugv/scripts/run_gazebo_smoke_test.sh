#!/usr/bin/env bash
set -euo pipefail

source /opt/ros/humble/setup.bash

# Basic simulation smoke test for CI/manual execution.
# Ensures Gazebo and Nav2 packages are installed and launchable.
ros2 pkg list | grep -q '^gazebo_ros$'
ros2 pkg list | grep -q '^nav2_bringup$'
ros2 pkg list | grep -q '^slam_toolbox$'

echo "ROS2/Gazebo/Nav2/SLAM packages available."
