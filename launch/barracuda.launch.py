import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    # Get the package directory
    pkg_barracuda_description = get_package_share_directory('barracuda_description')
    
    # Get the URDF via xacro
    robot_description_file = os.path.join(pkg_barracuda_description, 'urdf', 'barracuda.xacro')
    robot_description = ParameterValue(
        Command(['xacro ', robot_description_file]),
        value_type=str
    )
    
    # Include upload_barracuda launch file
    upload_barracuda_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_barracuda_description, 'launch', 'upload_barracuda.launch.py')
        )
    )
    
    # Joint state publisher node
    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        output='screen',
        parameters=[{
            'use_sim_time': False,
            'rate': 30
        }]
    )
    
    return LaunchDescription([
        upload_barracuda_launch,
        joint_state_publisher_node
    ])
