import random

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray


class ParkingSensorNode(Node):

    def __init__(self):
        super().__init__('parking_sensor')

        self.publisher = self.create_publisher(
            Float32MultiArray,
            '/parking_distances',
            10
        )

        self.timer = self.create_timer(
            1.0,
            self.publish_distances
        )

        self.get_logger().info(
            'Parking sensor node started successfully.'
        )

    def publish_distances(self):
        distances = [
            random.uniform(0.15, 2.50),
            random.uniform(0.15, 2.50),
            random.uniform(0.15, 2.50),
        ]

        message = Float32MultiArray()
        message.data = distances

        self.publisher.publish(message)

        self.get_logger().info(
            f'Left: {distances[0]:.2f} m | '
            f'Center: {distances[1]:.2f} m | '
            f'Right: {distances[2]:.2f} m'
        )


def main(args=None):
    rclpy.init(args=args)

    node = ParkingSensorNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()