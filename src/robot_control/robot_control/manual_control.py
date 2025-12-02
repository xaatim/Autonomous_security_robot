import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
from std_msgs.msg import String

class ManualControlNode(Node):
    def __init__(self):
        super().__init__('manual_control_node')
        self.cmd_vel_publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        
        self.joy_subscriber = self.create_subscription(
            Joy,
            'joy',
            self.joy_callback,
            10
        )
        self.mode_subscriber = self.create_subscription(
            String,
            'robot_mode',
            self.mode_callback,
            10
        )

        self.is_manual_mode = True 
        self.last_joy_msg = None
        
    def mode_callback(self, msg):
        self.is_manual_mode = (msg.data == "manual")
        if not self.is_manual_mode:
            self.cmd_vel_publisher.publish(Twist())

    def joy_callback(self, msg):
        self.last_joy_msg = msg
        
        if self.is_manual_mode:
            twist_msg = Twist()
            twist_msg.linear.x = self.last_joy_msg.axes[1]
            twist_msg.angular.z = self.last_joy_msg.axes[0] * 1.5
            self.cmd_vel_publisher.publish(twist_msg)

def main(args=None):
    rclpy.init(args=args)
    node = ManualControlNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()