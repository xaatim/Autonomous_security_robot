import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction, RegisterEventHandler
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch.event_handlers import OnProcessStart

from launch_ros.actions import Node


def generate_launch_description():
    package_name = 'scuttle_description'

    launch_robot = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory(
                package_name), 'launch', 'launch_robot.launch.py'
        )]))

    lidar_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory(
                package_name), 'launch', 'ydlidar.launch.py'
        )]))

    slam_toolbox_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory(
                "slam_toolbox"), 'launch', 'online_async_launch.py'
        )]), launch_arguments={'slam_params_file': os.path.join(
            get_package_share_directory(package_name), 'config', 'mapper_params_online_async.yaml'
        ), 'use_sim_time': 'false'}.items()
        
    )


    
    nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory(
                "nav2_bringup"), 'launch', 'navigation_launch.py'
        )]), launch_arguments={'use_sim_time': 'false', 'map_subscribe_transient_local': 'true'}.items()
    )



    # Launch them all!
    return LaunchDescription([
        launch_robot,
        lidar_launch,
        slam_toolbox_launch,
        nav2
    ])
