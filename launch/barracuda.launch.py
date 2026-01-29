import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    # Get the package directory
    pkg_barracuda_description = get_package_share_directory('barracuda_description')
    
    # Include upload_barracuda launch file
    upload_barracuda_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_barracuda_description, 'launch', 'upload_barracuda.launch.py')
        ),
        launch_arguments={'use_sim_time': 'false'}.items()
    )
    
    # Joint state publisher node
    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        namespace='barracuda',
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
