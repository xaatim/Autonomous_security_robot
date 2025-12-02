FROM ros:foxy-ros-base-focal

RUN apt-get update && apt-get install -y --no-install-recommends \
  ros-foxy-desktop=0.9.2-1* \
  && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
  git python3-pip python3-opencv libgtk-3-dev ros-foxy-cv-bridge wget
RUN pip install numpy==1.24.4
RUN pip install insightface==0.7.1
RUN pip install opencv-python-headless python-socketio websocket-client pyserial 
RUN apt-get install zlib1g

WORKDIR /home
COPY . /home


RUN apt-get install ./libcudnn8_8.2.1.32-1+cuda10.2_arm64.deb

RUN pip install onnxruntime_gpu-1.6.0-cp38-cp38-linux_aarch64.whl
# RUN pip install onnxruntime-gpu
RUN pip install python-dotenv
RUN usermod -aG video root
RUN usermod -aG dialout root


RUN colcon build

RUN echo "source /opt/ros/foxy/setup.bash" >> ~/.bashrc
RUN echo "source /home/install/setup.bash" >> ~/.bashrc
RUN echo  'export PATH=/usr/local/cuda-10.2/bin:$PATH' >>~/.bashrc
RUN echo 'export LD_LIBRARY_PATH=/usr/local/cuda-10.2/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc


CMD ["bash"]
