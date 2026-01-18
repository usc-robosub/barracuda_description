FROM ghcr.io/usc-robosub/dave-base:main

# Install xacro
RUN apt-get update && apt-get install -y \
    ros-noetic-xacro \
    && rm -rf /var/lib/apt/lists/*

# COPY . /opt/barracuda-simulation
COPY entrypoint.sh /entrypoint.sh

RUN . /opt/ros/noetic/setup.sh \ 
    && cd /opt/barracuda-simulation/catkin_ws \
    && catkin build

# Set working directory
WORKDIR /opt/barracuda-simulation/catkin_ws

# Source the workspace on container start
CMD ["/bin/bash", "/entrypoint.sh"]

