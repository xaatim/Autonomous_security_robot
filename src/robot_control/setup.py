from glob import glob
import os
from setuptools import find_packages, setup

package_name = 'robot_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='hatim',
    maintainer_email='xayari229@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'manual_control = robot_control.manual_control:main',
            'motor_driver = robot_control.motor_driver:main',
            'autonomous_control = robot_control.autonomous_control:main',
            'mode_manager = robot_control.mode_manager:main',
        ],
    },
)
