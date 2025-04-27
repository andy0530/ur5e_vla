#!/usr/bin/env python3
from launch import LaunchDescription
from launch.actions import SetEnvironmentVariable, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # Package share directories
    ur5e_share = FindPackageShare('ur5e_vla')
    ros_gz_share = FindPackageShare('ros_gz_sim')

    # Paths to resources
    xacro_file = PathJoinSubstitution([ur5e_share, 'urdf', 'ur5e.urdf.xacro'])
    gz_sim_launch = PathJoinSubstitution([ros_gz_share, 'launch', 'gz_sim.launch.py'])
    models_path = PathJoinSubstitution([ur5e_share, 'models'])
    meshes_path = PathJoinSubstitution([ur5e_share, 'meshes'])

    return LaunchDescription([
        # Ensure Gazebo finds both models/ and meshes/ directories
        SetEnvironmentVariable(
            name='GZ_SIM_RESOURCE_PATH',
            value=[meshes_path, ':', models_path]
        ),

        # Launch Gazebo Harmonic with Ogre rendering
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(gz_sim_launch),
            launch_arguments={'gz_args': '--render-engine ogre'}.items()
        ),

        # Publish URDF to /robot_description
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{
                'robot_description': Command([
                    FindExecutable(name='xacro'), ' ', xacro_file
                ]),
                'use_sim_time': True
            }]
        ),
 
        # Spawn UR5e by reading /robot_description
        Node(
            package='ros_gz_sim',
            executable='create',
            name='spawn_ur5e',
            output='screen',
            arguments=[
                '-topic', 'robot_description',
                '-name', 'ur5e',
                '-x', '0', '-y', '0', '-z', '0.1'
            ]
        ),
    ])
