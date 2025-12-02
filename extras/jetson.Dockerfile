FROM nvcr.io/nvidia/l4t-base:r32.7.1

RUN pip install numpy==1.24.4
RUN pip install insightface==0.7.1
RUN pip install opencv-python-headless


WORKDIR /home
COPY . /home


RUN pip install onnxruntime_gpu-1.6.0-cp38-cp38-linux_aarch64.whl

RUN usermod -aG video root
RUN usermod -aG dialout root

RUN echo  'export PATH=/usr/local/cuda-10.2/bin:$PATH' >>~/.bashrc
RUN echo 'export LD_LIBRARY_PATH=/usr/local/cuda-10.2/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc

CMD ["bash"]