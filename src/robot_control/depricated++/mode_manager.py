import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from std_msgs.msg import String
MINUS_BTN = 6
PLUS_BTN = 7
TIMER = 0.5

ROBOT_MODE = ['autonomous', 'manual']


class mode_manager(Node):
    def __init__(self):
        super().__init__("mode_manager")
        
        self.joy_sub = self.create_subscription(
            Joy, '/joy', self.joy_callback, 10)
        self.mode_pub = self.create_publisher(String, '/robot_mode', 1)
        self.timer = self.create_timer(TIMER, self.publisher_callback)
        self.msg = String()
        
    def publisher_callback(self):
        self.mode_pub.publish(self.msg)

    def joy_callback(self, data: Joy):
        if data.buttons[MINUS_BTN] == 1:
            print('minus')
            self.msg.data = ROBOT_MODE[0]
            return
        if data.buttons[PLUS_BTN] == 1:
            print('plus')
            self.msg.data = ROBOT_MODE[1]
            return
        # print('button pressed')


def main():

    rclpy.init()
    node = mode_manager()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
