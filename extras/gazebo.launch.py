import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro


def generate_launch_description():

    scuttle_bot_pkg_share = get_package_share_directory('scuttle_bot')
    gazebo_ros_pkg_share = get_package_share_directory('gazebo_ros')

    # --- 1. DEFINE FILE PATHS ---
    # MODIFIED: Point to the new .xacro file
    urdf_file_path = os.path.join(
        scuttle_bot_pkg_share, 'urdf', 'scuttle_bot.urdf.xacro')

    world_file_path = os.path.join(
        scuttle_bot_pkg_share, 'worlds', 'model.sdf')

    # This is the path to your controllers file
    controllers_yaml_path = os.path.join(
        scuttle_bot_pkg_share, 'config', 'controllers.yaml'
    )

    # ADDED: Path to your twist_mux config
    twist_mux_yaml_path = os.path.join(
        scuttle_bot_pkg_share, 'config', 'twist_mux.yaml'
    )

    # --- 2. PROCESS THE URDF WITH XACRO ---
    doc = xacro.parse(open(urdf_file_path))

    # MODIFIED: Pass 'use_sim_time': 'true' to load sim hardware
    xacro.process_doc(doc, mappings={
        'controllers_path': controllers_yaml_path,
        'use_sim_time': 'true'
    })

    robot_description_content = doc.toxml()  # type: ignore

    # --- 3. STANDARD LAUNCH NODES ---
    start_gazebo_world = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_ros_pkg_share, 'launch', 'gazebo.launch.py')
        ),
        launch_arguments={'world': world_file_path}.items()
    )

    static_tf_pub = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='tf_footprint_base',
        arguments=['--x', '0', '--y', '0', '--z', '0',
                   '--yaw', '0', '--pitch', '0', '--roll', '0',
                   '--frame-id', 'base_link', '--child-frame-id', 'base_footprint']
    )

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description_content,
            'use_sim_time': True  # This is correct for Gazebo
        }]
    )

    spawn_model = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='spawn_model',
        output='screen',
        arguments=[
            '-entity', 'scuttle_bot',
            '-topic', 'robot_description'
        ]
    )

    # --- 4. ROS2_CONTROL SPAWNER NODES ---
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster",
                   "--controller-manager", "/controller_manager"],
        output="screen",
    )

    diff_drive_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_drive_controller",
                   "--controller-manager", "/controller_manager"],
        output="screen",
    )

    # --- 5. ADDED CONTROL NODES (JOYSTICK & TWIST_MUX) ---

    # Twist Mux
    twist_mux = Node(
        package="twist_mux",
        executable="twist_mux",
        # Use sim time and load your twist_mux config
        parameters=[twist_mux_yaml_path, {'use_sim_time': True}],
        output="screen",
        # Remap its output to the controller's input
        remappings=[
            ('/cmd_vel_out', '/diff_drive_controller/cmd_vel_unstamped')]
    )

    # Joystick Driver Node
    joy_node = Node(
        package='joy',
        executable='joy_node',
        name='joy_node',
        parameters=[{
            'dev': '/dev/input/event5',  # Your controller port
            'deadzone': 0.1,
            'use_sim_time': True  # Tell it to use sim time
        }]
    )

    # Teleop Twist Joy Node
    teleop_twist_joy_node = Node(
        package='teleop_twist_joy',
        executable='teleop_node',
        name='teleop_twist_joy_node',
        parameters=[{
            'enable_button': 5,
            'axis_linear.x': 1,      # forward/back on left stick vertical
            'axis_angular.yaw': 0,   # left/right on left stick horizontal
            'scale_linear.x': 1.0,
            'scale_angular.yaw': 1.5,
            'use_sim_time': True  # Tell it to use sim time
        }],
        # Remap output to the correct twist_mux topic
        remappings=[('/cmd_vel', '/cmd_vel_joy')]
    )

    # --- 6. RETURN THE LAUNCH DESCRIPTION ---
    return LaunchDescription([
        start_gazebo_world,
        static_tf_pub,
        robot_state_publisher_node,
        spawn_model,
        joint_state_broadcaster_spawner,
        diff_drive_controller_spawner,

        # Add the new nodes to the launchr
        twist_mux,
        joy_node,
        teleop_twist_joy_node,
    ])
