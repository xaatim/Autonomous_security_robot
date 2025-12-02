import sys
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge
import socketio
import os
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import time
import threading

class socketio_node(Node):
    def __init__(self):
        super().__init__('socketio_node')
        self.image_sub = self.create_subscription(Image, "video_frames", self.listiner_callback, 1)
        self.remote_control_pub = self.create_publisher(String, 'robot_mode', 1)
        self.remote_control_sub = self.create_subscription(String, 'robot_mode', self.subscriper_callback, 1)
        self.cmd_vel_publisher = self.create_publisher(Twist, 'cmd_vel', 100)
        self.br = CvBridge()

        self.io = socketio.Client(reconnection=True, reconnection_delay=0)
        self.robot_id = os.getenv("serialNo")
        self.robot_key = os.getenv("robotKey")

        self.last_status_emit = 0  
        self.last_status_value = None

        self.io.connect(
            'https://wzx5svn0-4000.asse.devtunnels.ms/',
            auth={'serialNo': "BR100-SN-0014", 'robotKey': 'fmw3icuareacx1t0zuo3il'},
            wait=False,
        )
        self.events()

    def events(self):
        @self.io.event
        def connect():
            print("Connected to server.")

        @self.io.event
        def disconnect():
            print("Disconnected from server.")

        def controlMode(data):
            mode = data.get("mode")
            if mode:
                msg = String()
                msg.data = mode
                self.remote_control_pub.publish(msg)

            if mode == 'manual':
                twist = data.get("twist")
                if twist:
                    msg = Twist()
                    msg.linear.x = float(twist.get('x', 0))
                    msg.angular.z = float(twist.get('z', 0))  # fixed angular.z instead of linear.z
                    self.cmd_vel_publisher.publish(msg)

        self.io.on("robot:controlMode", controlMode)

    def subscriper_callback(self, msg: String):
        now = time.time()
        status = msg.data

        # Limit status updates to 5 per second
        if status != self.last_status_value or now - self.last_status_emit > 1.0:
            self.last_status_emit = now
            self.last_status_value = status
            self.io.start_background_task(self._emit_status, status)

    def _emit_status(self, data):
        try:
            if self.io.connected:
                self.io.emit("robot:status", data)
        except Exception as e:
            pass

    def listiner_callback(self, data: Image):
        recieved_frame = self.br.imgmsg_to_cv2(data, desired_encoding="bgr8")
        _, buf = cv2.imencode('.jpg', recieved_frame)
        self.io.emit('robot:frame', buf.tobytes())

def main():
    try:
        rclpy.init()
        node = socketio_node()
        rclpy.spin(node)
        node.destroy_node()
        rclpy.shutdown()
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == '__main__':
    main()
