#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray, String

class ElevatorControllerNode(Node):
    def __init__(self):
        super().__init__('elevator_controller')

        self.publisher = self.create_publisher(Float64MultiArray, '/position_controller/commands', 10)
        self.up_subscription = self.create_subscription(String, '/elevator_up', self.elevator_up_callback, 10)
        self.down_subscription = self.create_subscription(String, '/elevator_down', self.elevator_down_callback, 10)

    def elevator_up_callback(self, msg):
        cmd_msg = Float64MultiArray()
        cmd_msg.data = [0.3]
        self.publisher.publish(cmd_msg)

    def elevator_down_callback(self, msg):
        cmd_msg = Float64MultiArray()
        cmd_msg.data = [0.0]
        self.publisher.publish(cmd_msg)

def main(args=None):
    rclpy.init(args=args)

    node = ElevatorControllerNode()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
