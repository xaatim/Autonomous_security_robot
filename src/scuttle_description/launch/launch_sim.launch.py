import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, RegisterEventHandler
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.event_handlers import OnProcessExit

from launch_ros.actions import Node

def generate_launch_description():

    package_name='scuttle_description' 

    # 1. Launch RSP
    # We set use_sim_time=true. 
    # RSP will pass this to Xacro as "sim_mode=true", making joints CONTINUOUS (Physics enabled).
    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','rsp.launch.py'
                )]), launch_arguments={'use_sim_time': 'true', 'use_ros2_control': 'true'}.items()
    )

    # 2. Launch Gazebo
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
             )

    # 3. Spawn Robot
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'my_bot'],
                        output='screen')

    # 4. Controllers (Spawners)
    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_cont"],
    )

    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_broad"],
    )

    # 5. Delays (CRITICAL FOR GAZEBO)
    # Wait for spawn_entity to finish before starting the controllers
    # This prevents the "Controller Manager not found" error.
    delayed_diff_drive_spawner = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=spawn_entity,
            on_exit=[diff_drive_spawner],
        )
    )

    delayed_joint_broad_spawner = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=spawn_entity,
            on_exit=[joint_broad_spawner],
        )
    )
    
    joy_node = Node(
        package='joy',
        executable='joy_node',
        name='joy_node',
        parameters=[{
            'dev': '/dev/input/by-id/usb-Nintendo_Co.__Ltd._Pro_Controller_000000000001-event-joystick ', # Ensure this path is correct for your joystick
            'deadzone': 0.3,
        }]
    )
    
    teleop_twist_joy_node = Node(
        package='teleop_twist_joy',
        executable='teleop_node',
        name='teleop_twist_joy_node',
        parameters=[{
            'enable_button': 5,
            'axis_linear.x': 1,
            'axis_angular.yaw': 0,
            'scale_linear.x': -1.0,
            'scale_angular.yaw': 1.0
        }],
        remappings=[('cmd_vel', 'cmd_vel_joy')]
    )

    return LaunchDescription([
        rsp,
        gazebo,
        spawn_entity,
        delayed_diff_drive_spawner,
        delayed_joint_broad_spawner,
        joy_node,
        teleop_twist_joy_node
    ])