import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    # Get the package directory
    pkg_barracuda_description = get_package_share_directory('barracuda_description')
    
    # Declare arguments
    namespace_arg = DeclareLaunchArgument(
        'namespace',
        default_value='barracuda',
        description='Namespace for the robot'
    )
    
    debug_arg = DeclareLaunchArgument(
        'debug',
        default_value='false',
        description='Debug flag'
    )
    
    robot_description_file_arg = DeclareLaunchArgument(
        'robot_description_file',
        default_value=os.path.join(pkg_barracuda_description, 'urdf', 'barracuda.xacro'),
        description='Path to robot description file'
    )
    
    # Get the URDF via xacro
    robot_description = ParameterValue(
        Command(['xacro ', LaunchConfiguration('robot_description_file')]),
        value_type=str
    )
    
    # Robot state publisher node
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': True
        }],
        remappings=[
            ('/tf', '/barracuda/tf'),
            ('/tf_static', '/barracuda/tf_static')
        ]
    )
    
    return LaunchDescription([
        namespace_arg,
        debug_arg,
        robot_description_file_arg,
        robot_state_publisher_node
    ])
