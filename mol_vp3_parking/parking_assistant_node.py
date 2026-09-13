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

    def create_proximity_bar(self, distance):
        min_distance = 0.15
        max_distance = 2.50
        bar_length = 16

        clamped_distance = max(
            min(distance, max_distance),
            min_distance
        )

        proximity = (
            (max_distance - clamped_distance)
            / (max_distance - min_distance)
        )

        filled_length = round(
            proximity * bar_length
        )

        empty_length = bar_length - filled_length

        return (
            '['
            + '#' * filled_length
            + '-' * empty_length
            + ']'
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

        left_bar = self.create_proximity_bar(
            distances[0]
        )
        center_bar = self.create_proximity_bar(
            distances[1]
        )
        right_bar = self.create_proximity_bar(
            distances[2]
        )

        visualization = (
            '\n'
            '========== PARKING ASSISTANT ==========\n'
            f'LEFT    {left_bar} {distances[0]:.2f} m\n'
            f'CENTER  {center_bar} {distances[1]:.2f} m\n'
            f'RIGHT   {right_bar} {distances[2]:.2f} m\n'
            '\n'
            f'Closest obstacle: {closest_direction}\n'
            f'Status: {status}\n'
            '=======================================\n'
        )

        self.get_logger().info(visualization)


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