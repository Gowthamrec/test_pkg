import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration, Command
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')

    # Get package path
    pkg_path = get_package_share_directory('test_pkg')
    xacro_file = os.path.join(pkg_path, 'urdf', 'main.urdf.xacro')

    # Ensure xacro command is correctly formatted
    robot_description_config = ParameterValue(Command(['xacro ', xacro_file, ' sim_mode:=', use_sim_time]), value_type=str)

    # Parameters for robot_state_publisher
    params = {'robot_description': robot_description_config, 'use_sim_time': use_sim_time}
    
    # Robot State Publisher Node
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params]
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation time if true'
        ),
        node_robot_state_publisher
    ])
