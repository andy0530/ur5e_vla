from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import SetEnvironmentVariable, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch.substitutions import Command
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # Paths
    gz_sim_pkg_path = get_package_share_directory('ros_gz_sim')
    ur5e_pkg_share = FindPackageShare('ur5e_vla')
    urdf_xacro_path = PathJoinSubstitution([ur5e_pkg_share, 'urdf', 'ur5e.urdf.xacro'])
    sdf_model_path = PathJoinSubstitution([ur5e_pkg_share, 'models', 'ur5e', 'model.sdf'])
    gz_launch_path = PathJoinSubstitution([gz_sim_pkg_path, 'launch', 'gz_sim.launch.py'])

    return LaunchDescription([
        # Set GZ_SIM_RESOURCE_PATH to find meshes
        SetEnvironmentVariable(
            name='GZ_SIM_RESOURCE_PATH',
            value=PathJoinSubstitution([ur5e_pkg_share])
        ),

        # Launch Gazebo
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(gz_launch_path),
            launch_arguments={
                'gz_args': '--render-engine ogre'
            }.items()
        ),

        # Spawn UR5e in simulation
        Node(
            package='ros_gz_sim',
            executable='create',
            name='spawn_ur5e',
            output='screen',
            arguments=[
                '-name', 'ur5e',
                '-file', sdf_model_path,
                '-x', '0', '-y', '0', '-z', '0.1'
            ]
        )
    ])
