import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction, RegisterEventHandler
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch.event_handlers import OnProcessStart
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.actions import Node


def generate_launch_description():
    package_name = 'scuttle_description'

    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory(
                package_name), 'launch', 'rsp.launch.py'
        )]), launch_arguments={'use_sim_time': 'false', 'use_ros2_control': 'true'}.items()
    )


    
    robot_description = Command(
        ['ros2 param get --hide-type /robot_state_publisher robot_description'])
    
    controller_params_file = os.path.join(
        get_package_share_directory(package_name), 'config', 'controller.yaml')

    controller_manager = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[{'robot_description': ParameterValue(robot_description,value_type=str)},
                    controller_params_file],
        remappings=[
            ("~/robot_description", "/robot_description"),
        ],
    )

    delayed_controller_manager = TimerAction(
        period=3.0, actions=[controller_manager])

    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_cont"],
    )

    delayed_diff_drive_spawner = RegisterEventHandler(
        event_handler=OnProcessStart(
            target_action=controller_manager,
            on_start=[diff_drive_spawner],
        )
    )

    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_broad"],
    )

    delayed_joint_broad_spawner = RegisterEventHandler(
        event_handler=OnProcessStart(
            target_action=controller_manager,
            on_start=[joint_broad_spawner],
        )
    )

    # 5. Joystick Nodes
    joy_node = Node(
        package='joy',
        executable='joy_node',
        name='joy_node',
        parameters=[{
            'dev': '/dev/input/by-id/usb-Nintendo_Co.__Ltd._Pro_Controller_000000000001-event-joystick ',
            'deadzone': 0.3,
        }]
    )

    twist_mux_params = os.path.join(get_package_share_directory(
        package_name), 'config', 'twist_mux.yaml')
    twist_mux = Node(
        package="twist_mux",
        executable="twist_mux",
        parameters=[twist_mux_params, {'use_sim_time': False}],
        remappings=[('/cmd_vel_out', '/diff_cont/cmd_vel_unstamped')]
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

    # Launch them all!
    return LaunchDescription([
        rsp,
        twist_mux,
        delayed_controller_manager,
        delayed_diff_drive_spawner,
        delayed_joint_broad_spawner,
        joy_node,
        teleop_twist_joy_node
    ])
