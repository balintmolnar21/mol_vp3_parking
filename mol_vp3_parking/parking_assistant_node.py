import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray


class ParkingAssistantNode(Node):

    def __init__(self):
        super().__init__('parking_assistant')

        self.subscription = self.create_subscription(
            Float32MultiArray,
            '/parking_distances',
            self.distance_callback,
            10
        )

        self.get_logger().info(
            'Parking assistant node started successfully.'
        )

    def distance_callback(self, message):
        distances = message.data

        if len(distances) != 3:
            self.get_logger().warning(
                'Expected exactly three distance values.'
            )
            return

        directions = [
            'LEFT',
            'CENTER',
            'RIGHT'
        ]

        minimum_distance = min(distances)

        minimum_index = distances.index(
            minimum_distance
        )

        closest_direction = directions[minimum_index]

        self.get_logger().info(
            f'Received distances -> '
            f'Left: {distances[0]:.2f} m | '
            f'Center: {distances[1]:.2f} m | '
            f'Right: {distances[2]:.2f} m | '
            f'Closest obstacle: {closest_direction} '
            f'({minimum_distance:.2f} m)'
        )


def main(args=None):
    rclpy.init(args=args)

    node = ParkingAssistantNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()