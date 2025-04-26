from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'ur5e_vla'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        (os.path.join('share', 'ament_index', 'resource_index', 'packages'),
            [os.path.join('resource', package_name)]),
        (os.path.join('share', package_name), ['package.xml']),
        
        # Launch files
        (os.path.join('share', package_name, 'launch'), 
            glob(os.path.join('launch', '*.launch.py'))),

        # URDF and XACRO
        (os.path.join('share', package_name, 'urdf'),
            glob(os.path.join('urdf', '**', '*.urdf'), recursive=True) +
            glob(os.path.join('urdf', '**', '*.xacro'), recursive=True)),

        # SDF model files
        (os.path.join('share', package_name, 'models', 'ur5e'),
            glob(os.path.join('models', 'ur5e', '*.sdf')) +
            glob(os.path.join('models', 'ur5e', '*.config'))),

        # World files
        (os.path.join('share', package_name, 'worlds'),
            glob(os.path.join('worlds', '*.sdf')) +
            glob(os.path.join('worlds', '*.world')) +
            glob(os.path.join('worlds', '*.model'))),

        # Meshes
        (os.path.join('share', package_name, 'meshes'),
            glob(os.path.join('meshes', '**', '*.*'), recursive=True)),

        # Config
        (os.path.join('share', package_name, 'config'),
            glob(os.path.join('config', '**', '*.*'), recursive=True)),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Andy Lee',
    maintainer_email='andyjhlee0530@gmail.com',
    description='Simulation and control setup for UR5e with VLA (YOLO + pi0 integration planned)',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [],
    },
)
