#!/usr/bin/env bash
set -euo pipefail

source /opt/ros/humble/setup.bash

# Start SLAM in background
ros2 launch slam_toolbox online_async_launch.py \
  slam_params_file:=/app/ros2/params/slam_toolbox.yaml >/tmp/ugv_slam.log 2>&1 &

# Start Nav2 with static map
ros2 launch nav2_bringup navigation_launch.py \
  params_file:=/app/ros2/params/nav2_params.yaml \
  map:=/app/ros2/maps/residential_map.yaml >/tmp/ugv_nav2.log 2>&1 &

echo "UGV ROS2 stack started (SLAM + Nav2). Logs: /tmp/ugv_slam.log /tmp/ugv_nav2.log"
