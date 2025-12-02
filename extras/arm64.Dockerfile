FROM arm64v8/ros:humble-ros-base

RUN apt-get update && apt-get install -y \
  git python3-pip python3-opencv libgtk-3-dev ros-humble-cv-bridge ros-humble-joy

RUN pip install numpy==1.26.4 insightface==0.7.3
RUN pip install opencv-python-headless==4.9.0.80
RUN pip install python-socketio websocket-client pyserial
RUN pip install onnxruntime


COPY . /home

RUN usermod -aG video root
RUN usermod -aG dialout root

RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
RUN echo "source /home/install/setup.bash" >> ~/.bashrc


CMD ["bash"]
