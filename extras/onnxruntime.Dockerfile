FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y \
    build-essential git cmake python3.10-dev python3.10-venv \
    libopenblas-dev libprotobuf-dev protobuf-compiler \
    python3-pip curl wget \
    cuda-toolkit-10-2 libcudnn8 libcudnn8-dev \
    && rm -rf /var/lib/apt/lists/*

RUN git clone --recursive https://github.com/microsoft/onnxruntime.git /onnxruntime
WORKDIR /onnxruntime
RUN git checkout v1.16.0

RUN python3.10 -m venv build_env
RUN . build_env/bin/activate && pip install numpy wheel packaging
RUN . build_env/bin/activate && ./build.sh --config Release --update --build --parallel \
    --build_wheel --use_cuda \
    --cuda_home /usr/local/cuda \
    --cudnn_home /usr/lib/aarch64-linux-gnu \
    --enable_pybind \
    --allow_running_as_root
