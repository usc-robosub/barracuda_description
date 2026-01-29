# Barracuda Description - ROS2 Migration

This branch contains the ROS2 migration of the barracuda_description package.

## Changes from ROS1

### Package Configuration
- Updated `package.xml` to format 3 with `ament_cmake` as buildtool
- Converted `CMakeLists.txt` to use `ament_cmake` instead of `catkin`
- Standardized naming from `barracuda-description` to `barracuda_description`

### Launch Files
All launch files have been converted from XML to Python format:
- `upload_barracuda.launch` → `upload_barracuda.launch.py`
- `barracuda.launch` → `barracuda.launch.py`
- `barracuda_gazebo.launch` → `barracuda_gazebo.launch.py`

Old XML launch files are kept for reference but should not be used in ROS2.

### URDF/Xacro Files
- URDF and xacro files remain largely unchanged
- `$(find package_name)` syntax is still supported in ROS2

## Building

```bash
cd catkin_ws  # Will need to be renamed to ros2_ws
colcon build --packages-select barracuda_description
source install/setup.bash
```

## Usage

### Basic Launch
```bash
ros2 launch barracuda_description barracuda.launch.py
```

### Gazebo Launch
```bash
ros2 launch barracuda_description barracuda_gazebo.launch.py
```

### With Parameters
```bash
ros2 launch barracuda_description upload_barracuda.launch.py namespace:=barracuda
```

## Dependencies

Note: Some ROS1 dependencies like `dave_worlds` and `dave_nodes` may not be available in ROS2 yet. The gazebo launch file may need to be adapted based on available ROS2 underwater simulation packages.

## Migration Notes

1. **Workspace Structure**: Consider renaming `catkin_ws` to `ros2_ws` for clarity
2. **UUV Simulator**: Check if UUV simulator packages are available for ROS2
3. **DAVE**: The DAVE (Deep Autonomous Vehicles Environment) packages may need ROS2 ports
4. **Gazebo**: ROS2 uses Gazebo 11+ with `gazebo_ros_pkgs` for ROS2

## TODO

- [ ] Test launch files with actual ROS2 installation
- [ ] Verify Gazebo integration with ROS2
- [ ] Check UUV simulator compatibility
- [ ] Update Docker configuration for ROS2
