import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration, Command
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue # <--- NEW IMPORT

def generate_launch_description():

    # 1. Declare Arguments
    # We use 'use_sim_time' to control BOTH the time source and the URDF structure
    use_sim_time = LaunchConfiguration('use_sim_time')
    use_ros2_control = LaunchConfiguration('use_ros2_control')

    pkg_path = get_package_share_directory('scuttle_description')
    
    # POINT THIS TO YOUR MAIN XACRO FILE
    # Based on your messages, your main file seems to be 'scuttle_urdf.xacro' or 'scuttle.urdf.xacro'
    # Adjust the filename string below to match exactly what is in your folder.
    xacro_file = os.path.join(pkg_path, 'urdf', 'scuttle_urdf.xacro')

    # 2. Process the Xacro
    # MAGIC HAPPENS HERE: We map 'sim_mode' to the value of 'use_sim_time'
    robot_description_config = Command([
        'xacro ', xacro_file, 
        ' use_ros2_control:=', use_ros2_control, 
        ' sim_mode:=', use_sim_time
    ])
    
    # 3. Create the Robot State Publisher
    # FIX: We wrap the Command in ParameterValue(..., value_type=str)
    # This prevents the "Unable to parse ... as yaml" error
    params = {
        'robot_description': ParameterValue(robot_description_config, value_type=str), 
        'use_sim_time': use_sim_time
    }
    
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params]
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use sim time if true'),
        DeclareLaunchArgument(
            'use_ros2_control',
            default_value='true',
            description='Use ros2_control if true'),

        node_robot_state_publisher
    ])