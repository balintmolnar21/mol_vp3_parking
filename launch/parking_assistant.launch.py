from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='mol_vp3_parking',
            executable='parking_sensor',
            name='parking_sensor',
            output='screen'
        ),

        Node(
            package='mol_vp3_parking',
            executable='parking_assistant',
            name='parking_assistant',
            output='screen'
        ),
    ])