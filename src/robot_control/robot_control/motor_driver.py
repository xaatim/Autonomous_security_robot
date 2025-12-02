import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import serial
import time
from std_msgs.msg import String
from rclpy.duration import Duration as Duration


class MotorDriverNode(Node):
    def __init__(self):
        super().__init__('motor_driver_node')
        self.subscription = self.create_subscription(
            Twist, 'cmd_vel', self.twist_callback, 10)
        self.mode_sub = self.create_subscription(
            String, '/robot_mode', self.mode_callback, 1)

        self.ser = None
        try:
            self.ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.1)
        except serial.SerialException as e:
            self.get_logger().error(f"Could not open serial port: {e}")

        self.last_command = None
        self.motor_timer = self.create_timer(0.01, self.timer_callback)
        self.last_send_time = self.get_clock().now()
        self.command_threshold = 1
        self.linear_x = 0
        self.angular_z = 0
        self.mode = None
    def mode_callback(self, msg: String):
        self.mode = msg.data
        if self.ser and self.ser.is_open:
            if self.mode == "autonomous":
                self.ser.write(bytes('A', 'utf-8'))
            if self.mode == 'manual':
                self.ser.write(bytes('M', 'utf-8'))
        else:
            self.get_logger().warn("Serial not ready to send mode command.")

    def twist_callback(self, twist_msg: Twist):
        self.linear_x = twist_msg.linear.x
        self.angular_z = twist_msg.angular.z

    def timer_callback(self):
        if self.ser is None or not self.ser.is_open:
            self.get_logger().warn('No serial detected. Cannot send command.')
            return

        command_char = None
        linear_threshold = 0.1
        angular_threshold = 0.1
        stopping_threshold = 0.0

        # if self.linear_x== stopping_threshold:
        #   command_char = 'q'
        #   print("stoped command")
        
        if self.linear_x > linear_threshold:
            command_char = 'f'
            print("forward command")
        elif self.linear_x < -linear_threshold:
            command_char = 'b'
            print("backward command")
        elif self.angular_z > angular_threshold:
            command_char = 'l'
            print("lefr command")
        elif self.angular_z < -angular_threshold:
            command_char = 'r'
            print("right command")
        else:
            command_char = 'q'
            print("anothwe stoped command")

        try:
            if command_char != self.last_command or self.get_clock().now() - self.last_send_time >= Duration(seconds=self.command_threshold):
                self.ser.write(bytes(command_char, 'utf-8'))
                self.last_command = command_char
                self.last_send_time = self.get_clock().now()
        except serial.SerialException as e:
            self.get_logger().error(
                f"Serial communication failed while writing: {e}")
            self.ser = None


def main():
    rclpy.init()
    node = MotorDriverNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
