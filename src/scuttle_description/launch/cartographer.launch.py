import os
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_name = 'scuttle_description' 
    pkg_share = get_package_share_directory(pkg_name)

    cartographer_config_dir = os.path.join(pkg_share, 'config')
    configuration_basename = 'scuttle_cartographer.lua'

    return LaunchDescription([
        
        # Cartographer Node
        Node(
            package='cartographer_ros',
            executable='cartographer_node',
            name='cartographer_node',
            output='screen',
            parameters=[{'use_sim_time': False}],
            remappings=[
                ('odom', '/diff_cont/odom'),
            ],
            arguments=[
                '-configuration_directory', cartographer_config_dir,
                '-configuration_basename', configuration_basename]),

        # Grid Node
        Node(
            package='cartographer_ros',
            executable='cartographer_occupancy_grid_node',
            name='cartographer_occupancy_grid_node',
            output='screen',
            parameters=[{'use_sim_time': False}],
            arguments=['-resolution', '0.05', '-publish_period_sec', '1.0']),
    ])