import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'scuttle_description'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*.py'))),
        
        (os.path.join('share', package_name, 'urdf'), glob(os.path.join('urdf/*'))),
        
        (os.path.join('share', package_name, 'rviz'), glob(os.path.join('rviz/*'))),
        
        (os.path.join('share', package_name, 'config'), glob(os.path.join('config/*'))),

        (os.path.join('share', package_name, 'meshes'), glob(os.path.join('meshes/*'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='hatim',
    maintainer_email='xayari229@gmail.com',
    description='Scuttle Robot Description Package for ROS 2',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        ],
    },
)