# 🤖 Autonomous Indoor Surveillance Robot (SCUTTLE-Intel AMR)

*A fully autonomous mobile security unit featuring LiDAR SLAM, biometric intruder detection, and cloud-native fleet integration.*

---

## 🤝 In Collaboration With

<a href="https://katapultasia.com/">
  <img src="https://katapultasia.com/wp-content/uploads/2020/06/katapult-logo.png" height="50" alt="Katapult Asia">
</a>

**Special thanks to Katapult Asia (Malaysia)** for providing the SCUTTLE-Intel AMR hardware platform and technical mentorship, enabling real-world validation of this project.

---

## 📖 Overview

This project implements a **modular indoor surveillance system** on the **SCUTTLE-Intel Autonomous Mobile Robot (AMR)**.  
Unlike traditional passive CCTV systems, this robot:

- Autonomously patrols indoor environments  
- Builds dynamic maps using SLAM  
- Actively identifies intruders using edge-computed deep learning  

The system is built on **ROS 2 Humble** and integrates:

- **Navigation**: Nav2 Stack & SLAM Toolbox for mapping and dynamic path planning  
- **Perception**: InsightFace for high-accuracy, real-time face recognition  
- **Security**: *Store-First Protocol* to secure forensic evidence locally before transmission  

---

## 🌐 Beam Robotics Integration (SaaS Ecosystem)

This autonomous unit serves as the **hardware flagship** for **Beam Robotics**, a co-founded initiative focused on secure, scalable robotic deployments with integrated monitoring dashboards.

Each robot pairs with the **Beam Robotics cloud infrastructure**, providing **exclusive and encrypted access per device owner**.

---

### 1. The Beam Platform (Home)

The central hub for Beam Robotics products.  
It manages the ecosystem of deployed robots and provides a unified entry point for hardware control and monitoring.

> *Above: Beam Robotics landing page*

---

### 2. Fleet Management & Robot Selection

After login, customers access a **private fleet interface** showing only robots registered to their account.

- **Exclusive Access**: Only the verified owner can access the robot dashboard  
- **Robot Registration**: Devices are added using a unique cryptographic key  
- **Customization**: Configure robot-specific add-ons (GPS, sensors, modules)

> *Above: Fleet selection interface*

---

### 3. Live Command Dashboard

Selecting a robot opens its **dedicated command center**:

- Encrypted, low-latency video feeds  
- Real-time alerts and telemetry  
- Secure access restricted to the verified owner  

> *Above: Active surveillance dashboard*

---

## 👁️ Computer Vision Performance

Our proprietary vision pipeline is optimized for real-world unpredictability and exceeds standard academic baselines.

### 1. Robustness to Environment

- Maintains high accuracy from **low-light environments (<50 lux)**  
- Performs reliably under **direct sunlight and harsh indoor lighting**

### 2. Advanced Occlusion Handling

- Detects and flags risks even when faces are **partially occluded** (e.g., masks)  
- Uses **facial geometry analysis**, not just texture matching

### 3. Tuning & Accuracy

- Validated on **200 real inference trials**  
- Achieved **0% False Acceptance Rate (FAR)** at optimal threshold

---

## 🎯 Key Technical Features

### 🧭 Autonomous Navigation

- **SLAM**: 2D occupancy grid generation using SLAM Toolbox  
- **Path Planning**: Nav2 (Behavior Trees) for dynamic obstacle avoidance  
- **Localization**: AMCL with ±5 cm pose accuracy  

### 🧠 Intelligent Perception

- **Face Recognition**: InsightFace + Cosine Similarity scoring  
- **Alert System**:
  - Captures images of *Unknown* individuals  
  - Stores evidence locally (*store-first protocol*)  
  - Sends automated email alerts  

### 🖥️ Hardware Control

- **Drive System**: Custom ROS 2 hardware interface (differential drive)  
- **Latency Optimization**:
  - Non-blocking surveillance threads  
  - ~110 ms average system latency  

---

## 🧰 Tech Stack & Hardware

### 🔩 Hardware Core

- **Compute**: Axiomtek Embedded Computer (Intel Architecture)  
- **Chassis**: SCUTTLE-Intel AMR Kit (Differential Drive)  

### 📡 Sensors

- **LiDAR**: YDLIDAR X2 / X4 (2D scanning)  
- **Vision**: Intel RealSense D435i (RGB-D)

### ⚙️ Actuators

- Cytron DC Motors  
- MD10C Motor Drivers  

---

## 🧪 Software Architecture

- **OS**: Ubuntu 22.04 LTS (Jammy Jellyfish)  
- **Middleware**: ROS 2 Humble Hawksbill  
- **Languages**: Python 3.10, C++  
- **Libraries**:
  - `rclpy`
  - `nav2_simple_commander`
  - `insightface`
  - `opencv-python`
  - `smtplib`

---

## 🗂️ Repository Structure

```text
Autonomous-Security-Robot/
├── src/
│   ├── robot_kernel/          # Core system logic (launchers, integration)
│   ├── robot_vision/          # InsightFace logic, camera nodes, alerting
│   ├── generic_robot_driver/  # URDF models, hardware interfaces, params
│   └── ydlidar_ros2_driver/   # LiDAR sensor drivers
├── docs/
│   └── product_showcase/      # Product results & Beam platform screenshots
├── maps/                      # Saved SLAM maps (.yaml / .pgm)
├── docker/                    # Docker containers for deployment
└── README.md
```
---

## ⚙️ Installation

### 1. Prerequisites

* Ubuntu 22.04
* ROS 2 Humble installed and sourced

### 2. Setup Workspace

```
mkdir -p ~/scuttle_ws/src
cd ~/scuttle_ws/src
git clone https://github.com/xaatim/Autonomous-Security-Robot.git .
```

### 3. Install Dependencies

```
cd ~/scuttle_ws
rosdep update
rosdep install --from-paths src --ignore-src -r -y
pip install -r src/Autonomous_security_robot-myFyp-/requirements.txt
```

### 4. Build

```
colcon build --symlink-install
source install/setup.bash
```

---

## 🚀 Usage

### 1. Launch Robot (Hardware & Drivers)

```bash
ros2 launch generic_robot_driver scuttle_full.launch.py
```

### 2. Start Surveillance & Navigation

```bash
ros2 launch robot_kernel robot_control_launch.py
```

---

## 👥 Contributors

**Hatim Ahmed Hassan**
Lead Developer & Co-Founder (Beam Robotics)
📧 *Email*

---

## 🙏 Acknowledgments

* **Katapult Asia** — Hardware and technical mentorship

---

## 📄 License

This project is licensed under the **MIT License**.
See the `LICENSE` file for details.

