import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge

class camera_publisher(Node):
  def __init__(self):
    super().__init__('camera_pub')
    self.image_pub = self.create_publisher(Image,"video_frames",1)
    timer_period = 0.01
    self.create_timer(timer_period,self.publisher_callback)
  
    # self.cap = cv2.VideoCapture(r"/home/ros2_ws/src/Recording 2025-07-25 221211.mp4")
    self.cap = cv2.VideoCapture(0) # force v4l2 backend
    #self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G')) # type: ignore
    self.br = CvBridge()
    
  def publisher_callback(self):
    ret,frame = self.cap.read()
    if ret:
      self.image_pub.publish(self.br.cv2_to_imgmsg(frame,encoding='bgr8'))
#      cv2.imshow("f",frame)
#      cv2.waitKey(1)
      
    
    
    
def main():
  
  try: 
    print('publishing video frames..........')
    rclpy.init()
    cam_pub = camera_publisher()
    
    rclpy.spin(cam_pub)
    cam_pub.destroy_node()#optional
    rclpy.shutdown()
    
    
  except KeyboardInterrupt:
    print('exit 0 ')
    cam_pub.cap.release()
  
if __name__ == '__main__':
  main()