import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from std_msgs.msg import String
from geometry_msgs.msg import Twist


class manual_control(Node):
    def __init__(self):
        super().__init__("manual_control")
        
        self.joy_sub = self.create_subscription(
            Joy, '/joy', self.joy_callback, 10)        
        self.robot_mode_sub = self.create_subscription(
            String, '/robot_mode', self.robot_mode_callback, 10)
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 1)
        # self.timer = self.create_timer(TIMER, self.publisher_callback)
        self.msg = String()
    def robot_mode_callback(self,data):
      pass
    def publisher_callback(self):
        # self.mode_pub.publish(self.msg)
        ...

    def joy_callback(self, data: Joy):
        print(data)
        # if data.buttons[MINUS_BTN] == 1:
        #     print('minus')
        #     self.msg.data = ROBOT_MODE[0]
        #     return
        # if data.buttons[PLUS_BTN] == 1:
        #     print('plus')
        #     self.msg.data = ROBOT_MODE[1]
        #     return
        # # print('button pressed')


def main():

    rclpy.init()
    node = manual_control()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
