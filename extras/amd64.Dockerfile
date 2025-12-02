FROM osrf/ros:humble-desktop

RUN apt-get update && apt-get install -y \
  git python3-pip python3-opencv libgtk-3-dev ros-humble-cv-bridge 

RUN pip install numpy==1.26.4 opencv-python-headless==4.9.0.80 insightface==0.7.1 python-socketio websocket-client pyserial onnxruntime

WORKDIR /home
COPY . /home
RUN apt install xxd
RUN usermod -aG video root
RUN usermod -aG dialout root

RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc


CMD ["bash"]
