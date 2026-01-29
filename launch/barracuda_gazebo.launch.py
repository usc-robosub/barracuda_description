import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess
from launch.substitutions import LaunchConfiguration, Command
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.conditions import IfCondition
from launch_ros.actions import Node


def generate_launch_description():
    # Get the package directory
    pkg_barracuda_description = get_package_share_directory('barracuda_description')
    
    # Declare arguments
    gui_arg = DeclareLaunchArgument('gui', default_value='true')
    paused_arg = DeclareLaunchArgument('paused', default_value='false')
    namespace_arg = DeclareLaunchArgument('namespace', default_value='barracuda')
    velocity_control_arg = DeclareLaunchArgument('velocity_control', default_value='true')
    joy_id_arg = DeclareLaunchArgument('joy_id', default_value='0')
    debug_arg = DeclareLaunchArgument('debug', default_value='false')
    verbose_arg = DeclareLaunchArgument('verbose', default_value='false')
    x_arg = DeclareLaunchArgument('x', default_value='25')
    y_arg = DeclareLaunchArgument('y', default_value='0')
    z_arg = DeclareLaunchArgument('z', default_value='-85')
    roll_arg = DeclareLaunchArgument('roll', default_value='0')
    pitch_arg = DeclareLaunchArgument('pitch', default_value='0')
    yaw_arg = DeclareLaunchArgument('yaw', default_value='-1.8')
    
    # World file - Note: dave_worlds may need to be adapted for ROS2
    world_arg = DeclareLaunchArgument(
        'world_name',
        default_value='',  # Update with ROS2 world path when available
        description='Gazebo world file'
    )
    
    # Get the URDF via xacro
    robot_description_file = os.path.join(pkg_barracuda_description, 'urdf', 'barracuda.xacro')
    robot_description = Command(['xacro ', robot_description_file])
    
    # Start Gazebo server
    start_gazebo_server = ExecuteProcess(
        cmd=['gzserver',
             '--verbose',
             '-s', 'libgazebo_ros_init.so',
             '-s', 'libgazebo_ros_factory.so',
             LaunchConfiguration('world_name')],
        output='screen'
    )
    
    # Start Gazebo client
    start_gazebo_client = ExecuteProcess(
        cmd=['gzclient'],
        output='screen',
        condition=IfCondition(LaunchConfiguration('gui'))
    )
    
    # Spawn robot
    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', LaunchConfiguration('namespace'),
            '-topic', 'robot_description',
            '-x', LaunchConfiguration('x'),
            '-y', LaunchConfiguration('y'),
            '-z', LaunchConfiguration('z'),
            '-R', LaunchConfiguration('roll'),
            '-P', LaunchConfiguration('pitch'),
            '-Y', LaunchConfiguration('yaw')
        ],
        output='screen'
    )
    
    # Robot state publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        namespace=LaunchConfiguration('namespace'),
        output='screen',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': True
        }]
    )
    
    # Static transform from world to map
    world_to_map_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='world_to_map',
        arguments=['0', '0', '0', '0', '0', '0', 'world', 'map']
    )
    
    return LaunchDescription([
        gui_arg,
        paused_arg,
        world_arg,
        namespace_arg,
        velocity_control_arg,
        joy_id_arg,
        debug_arg,
        verbose_arg,
        x_arg,
        y_arg,
        z_arg,
        roll_arg,
        pitch_arg,
        yaw_arg,
        start_gazebo_server,
        start_gazebo_client,
        robot_state_publisher,
        spawn_robot,
        world_to_map_tf
    ])
