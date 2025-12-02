import cv2

width=1280
height=720
flip=2
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(width)+', height='+str(height)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam= cv2.VideoCapture(camSet)

while True: 
  ret,frame = cam.read()
  
  cv2.imshow("test",frame)
  
  if cv2.waitKey(1)==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()