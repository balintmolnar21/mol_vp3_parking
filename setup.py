from setuptools import find_packages, setup
from glob import glob
import os


package_name = 'mol_vp3_parking'


setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name]
        ),
        (
            'share/' + package_name,
            ['package.xml']
        ),
        (
            os.path.join('share', package_name),
            glob('launch/*launch.[pxy][yma]*')
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,

    maintainer='Molnar Balint',
    maintainer_email='molnar.balint.otto@gmail.com',

    description='ROS 2 based simulated parking assistant implemented in Python.',
    license='GNU General Public License v3.0',

    tests_require=['pytest'],

    entry_points={
        'console_scripts': [
            'parking_sensor = mol_vp3_parking.parking_sensor_node:main',
            'parking_assistant = mol_vp3_parking.parking_assistant_node:main',
        ],
    },
)