import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from std_msgs.msg import String

MINUS_BTN = 6
PLUS_BTN = 7

class ModeManager(Node):
    def __init__(self):
        super().__init__("mode_manager")
        
        self.current_mode = 'manual'
        self.mode_pub = self.create_publisher(String, '/robot_mode', 1)
        
        self.joy_sub = self.create_subscription(
            Joy, '/joy', self.joy_callback, 1)

    def joy_callback(self, data: Joy):
        if data.buttons[MINUS_BTN] == 1 and self.current_mode != 'autonomous':
            self.current_mode = 'autonomous'
            msg = String()
            msg.data = self.current_mode
            self.mode_pub.publish(msg)
            self.get_logger().info('Mode changed to: ' + self.current_mode)
        
        elif data.buttons[PLUS_BTN] == 1 and self.current_mode != 'manual':
            self.current_mode = 'manual'
            msg = String()
            msg.data = self.current_mode
            self.mode_pub.publish(msg)
            self.get_logger().info('Mode changed to: ' + self.current_mode)

def main(args=None):
    rclpy.init(args=args)
    node = ModeManager()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()