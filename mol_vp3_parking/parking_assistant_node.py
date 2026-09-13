import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import String


class ParkingAssistantNode(Node):

    def __init__(self):
        super().__init__('parking_assistant')

        self.subscription = self.create_subscription(
            Float32MultiArray,
            '/parking_distances',
            self.distance_callback,
            10
        )

        self.status_publisher = self.create_publisher(
            String,
            '/parking_status',
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
        minimum_index = distances.index(minimum_distance)
        closest_direction = directions[minimum_index]

        if minimum_distance > 1.0:
            status = 'SAFE'
        elif minimum_distance > 0.6:
            status = 'CAUTION'
        elif minimum_distance > 0.3:
            status = 'WARNING'
        else:
            status = 'STOP'

        output = (
            f'{status} | '
            f'Closest obstacle: {closest_direction} | '
            f'Distance: {minimum_distance:.2f} m'
        )

        status_message = String()
        status_message.data = output

        self.status_publisher.publish(status_message)

        self.get_logger().info(
            f'Left: {distances[0]:.2f} m | '
            f'Center: {distances[1]:.2f} m | '
            f'Right: {distances[2]:.2f} m | '
            f'{output}'
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