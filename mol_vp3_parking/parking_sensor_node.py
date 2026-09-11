import rclpy
from rclpy.node import Node


class ParkingSensorNode(Node):

    def __init__(self):
        super().__init__('parking_sensor')

        self.get_logger().info(
            'Parking sensor node started successfully.'
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