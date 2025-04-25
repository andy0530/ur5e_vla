from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import SetEnvironmentVariable, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Paths
    gz_sim_pkg_path = get_package_share_directory('ros_gz_sim')
    ur5e_pkg_path = FindPackageShare('ur5e_vla')
    gz_launch_path = PathJoinSubstitution([ur5e_pkg_path, 'launch', 'gz_sim.launch.py'])  # If you use the built-in sim, use: [gz_sim_pkg_path, 'launch', 'gz_sim.launch.py']

    return LaunchDescription([
        # Set model path so Gazebo can find your UR5e model
        SetEnvironmentVariable(
            name='GZ_SIM_RESOURCE_PATH',
            value=PathJoinSubstitution([ur5e_pkg_path, 'models'])
        ),

        # Include the standard Gazebo simulation launch
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(PathJoinSubstitution([gz_sim_pkg_path, 'launch', 'gz_sim.launch.py'])),
            launch_arguments={
                'gz_args': '--render-engine ogre'
            }.items()
        ),

        # Spawn UR5e into simulation
        Node(
            package='ros_gz_sim',
            executable='create',
            name='spawn_ur5e',
            output='screen',
            arguments=[
                '-name', 'ur5e',
                '-file', PathJoinSubstitution([ur5e_pkg_path, 'models', 'ur5e', 'model.sdf']),
                '-x', '0', '-y', '0', '-z', '0.1'
            ]
        ),

        # Optional: Bridge example (replace when needed)
        # Node(
        #     package='ros_gz_bridge',
        #     executable='parameter_bridge',
        #     arguments=['/example_topic@sensor_msgs/msg/Imu@gz.msgs.IMU'],
        #     remappings=[('/example_topic', '/remapped_topic')],
        #     output='screen'
        # ),
    ])
