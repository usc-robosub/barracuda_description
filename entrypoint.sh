#!/usr/bin/bash
source /opt/ros/noetic/setup.bash

source devel/setup.bash

rosrun xacro xacro /urdf/barracuda.xacro > /urdf/barracuda.urdf