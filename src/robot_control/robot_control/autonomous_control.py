import time
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String, Float64
from rclpy.duration import Duration as Duration


class AutonomousControlNode(Node):

    def __init__(self):
        super().__init__('autonomous_control_node')

        self.cmd_vel_publisher = self.create_publisher(Twist, 'cmd_vel', 1)
        self.mode_subscriber = self.create_subscription(
            String, 'robot_mode', self.mode_callback, 10)
        self.distance_subscriber = self.create_subscription(
            Float64, 'distance', self.distance_callback, 1)

        self.is_autonomous_mode = False
        self.obstacle_detected = False

        self.robot_state = "moving_forward"
        self.turn_start_time = None
        self.turn_duration = 1
        self.timer = self.create_timer(0.05, self.timer_callback)

    def mode_callback(self, msg):
        self.is_autonomous_mode = (msg.data == "autonomous")
        if not self.is_autonomous_mode:
            self.cmd_vel_publisher.publish(Twist())
            self.robot_state = "moving_forward"
            self.turn_start_time = None

    def distance_callback(self, msg):
        self.msg = msg
        self.obstacle_detected = (msg.data < 200)

    def timer_callback(self):
        if not self.is_autonomous_mode:
            return

        twist_msg = Twist()

        if self.robot_state == "moving_forward":
            if self.obstacle_detected:
                print("obstacle_detected:", time.time())
                twist_msg.linear.x = 0.0
                twist_msg.angular.z = 0.0
                self.cmd_vel_publisher.publish(twist_msg)
                self.robot_state = "turning"
                self.turn_start_time = self.get_clock().now()

            else:
                twist_msg.linear.x = 0.5
                print("obstacle_not detected:", time.time())
                twist_msg.angular.z = 0.0
                self.cmd_vel_publisher.publish(twist_msg)

        elif self.robot_state == "turning":
            if self.get_clock().now() - self.turn_start_time >= Duration(seconds=self.turn_duration):
                self.robot_state = "moving_forward"

            else:
                print("turning", time.time())
                twist_msg.linear.x = 0.0
                twist_msg.angular.z = -0.5
                self.cmd_vel_publisher.publish(twist_msg)


def main():
    rclpy.init()
    node = AutonomousControlNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
