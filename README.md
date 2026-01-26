Markdown

# 🤖 Autonomous Indoor Surveillance Robot (SCUTTLE-Intel AMR)

![ROS 2 Humble](https://img.shields.io/badge/ROS_2-Humble-34495E?logo=ros&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white)
![InsightFace](https://img.shields.io/badge/AI-InsightFace-green)
![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Status](https://img.shields.io/badge/Status-Stable-success)

> **A fully autonomous mobile security unit featuring LiDAR SLAM, biometric intruder detection, and cloud-native fleet integration.**

---

## 🤝 In Collaboration With

<a href="https://katapultasia.com/">
  <img src="https://katapultasia.com/wp-content/uploads/2020/06/katapult-logo.png" height="50" alt="Katapult Asia">
</a>

**Special thanks to [Katapult Asia](https://katapultasia.com/)** (Malaysia) for providing the SCUTTLE-Intel AMR hardware platform and technical mentorship, enabling the real-world validation of this project.

---

## 📖 Overview

This project implements a modular surveillance system on the **SCUTTLE-Intel Autonomous Mobile Robot (AMR)**. Unlike traditional passive CCTVs, this robot autonomously patrols indoor environments, builds dynamic maps, and actively identifies intruders using edge-computed deep learning.

The system is built on **ROS 2 Humble** and integrates:
* **Navigation:** Nav2 stack & SLAM Toolbox for mapping and dynamic path planning.
* **Perception:** **InsightFace** for high-accuracy, real-time face recognition.
* **Security:** A "Store-First" protocol that secures forensic evidence locally before transmission.

---

## 🌐 Beam Robotics Integration (SaaS Ecosystem)

This autonomous unit is designed to operate as the hardware flagship for **Beam Robotics**, a co-founded initiative focused on democratizing autonomous security.

The system is architected to pair seamlessly with the **Beam Robotics** cloud infrastructure. Rather than operating in isolation, the robot integrates with a centralized command center designed for fleet management and remote accessibility.

### 🔐 Secure Device Pairing
The architecture supports a "Key-Based" pairing protocol. Each physical robot is issued a cryptographically unique identity key. Clients can register their devices directly to the Beam platform, establishing a secure, encrypted link between the edge device (the robot) and the user account.

### 🖥️ Centralized Command Dashboard
Once paired, the robot synchronizes with the web-based dashboard. This interface allows clients to:
* View low-latency, encrypted video feeds from anywhere.
* Receive real-time intruder alerts and snapshots.
* Monitor device health and battery status remotely.

![Beam Robotics Platform](./docs/product_showcase/beam_platform_overview.png)
*Above: The Beam Robotics platform interface, demonstrating the centralized dashboard for managing paired security robots.*

---

## 👁️ Computer Vision Performance

Our proprietary vision pipeline is optimized for real-world unpredictability, outperforming standard educational baselines.

### 1. Robustness to Environment
The system maintains high accuracy in extreme lighting conditions, from low-light server rooms (<50 lux) to direct sunlight.

![Lighting Test](./docs/product_showcase/environmental_robustness.png)

### 2. Advanced Occlusion Handling
Unlike standard recognizers that fail with face masks, our system analyzes facial geometry to flag potential security risks or identify users with partial occlusion.

![Mask Test](./docs/product_showcase/occlusion_analysis.png)

### 3. Tuning & Accuracy
Calibrated on a validation set of 200 inference trials, we achieved a **0% False Acceptance Rate (FAR)** at our optimal threshold.

![Metrics](./docs/product_showcase/performance_metrics.png)

---

## 🎯 Key Technical Features

### 🧭 Autonomous Navigation
* **SLAM:** Generates 2D occupancy grid maps using **SLAM Toolbox**.
* **Path Planning:** Uses **Nav2** (Behavior Trees) for dynamic obstacle avoidance and waypoint patrolling.
* **Localization:** Adaptive Monte Carlo Localization (AMCL) for precise pose estimation (±5 cm accuracy).

### 🧠 Intelligent Perception
* **Face Recognition:** Utilizes `InsightFace` with Cosine Similarity scoring to distinguish between authorized personnel and intruders.
* **Alert System:** Automatically captures snapshots of "Unknown" individuals and stores them locally (`store-first` protocol) before sending email alerts.

### 🖥️ Hardware Control
* **Drive System:** Custom ROS 2 hardware interface for differential drive kinematics.
* **Latency Optimization:** Custom threading ensures surveillance logic does not block critical navigation control loops (110ms average latency).

---

## 🧰 Tech Stack & Hardware

### **Hardware Core**
* **Compute:** Axiomtek Embedded Computer (Intel Architecture)
* **Chassis:** SCUTTLE-Intel AMR Kit (Differential Drive)
* **Sensors:** * **LiDAR:** YDLIDAR X2/X4 (2D Scanning)
    * **Vision:** Intel RealSense D435i RGB-D Camera
* **Actuators:** Cytron DC Motors + MD10C Drivers

### **Software Architecture**
* **OS:** Ubuntu 22.04 LTS (Jammy Jellyfish)
* **Middleware:** ROS 2 Humble Hawksbill
* **Languages:** Python 3.10, C++
* **Libraries:** `rclpy`, `nav2_simple_commander`, `insightface`, `opencv-python`, `smtplib`.

---

## 🗂️ Repository Structure

```text
Autonomous-Security-Robot/
├── src/
│   ├── robot_kernel/          # Core system logic (launchers, integration)
│   ├── robot_vision/          # InsightFace logic, camera nodes, alerting
│   ├── generic_robot_driver/  # URDF models, hardware interfaces, params
│   └── ydlidar_ros2_driver/   # Lidar sensor drivers
├── docs/
│   └── product_showcase/      # Documentation assets & results
├── maps/                      # Saved SLAM maps (.yaml / .pgm)
├── docker/                    # Docker containers for deployment
└── README.md

⚙️ Installation
1. Prerequisites

Ensure you are running Ubuntu 22.04 with ROS 2 Humble installed.
2. Setup Workspace
Bash

mkdir -p ~/scuttle_ws/src
cd ~/scuttle_ws/src
git clone [https://github.com/xaatim/Autonomous-Security-Robot.git](https://github.com/xaatim/Autonomous-Security-Robot.git) .

3. Install Dependencies
Bash

cd ~/scuttle_ws
rosdep update
rosdep install --from-paths src --ignore-src -r -y
pip install -r src/Autonomous_security_robot-myFyp-/requirements.txt

4. Build
Bash

colcon build --symlink-install
source install/setup.bash

🚀 Usage
1. Launch Robot (Hardware & Drivers)

Bring up the motors, LiDAR, and camera drivers:
Bash

ros2 launch generic_robot_driver scuttle_full.launch.py

2. Start Surveillance & Navigation

Launch the navigation stack and face recognition nodes:
Bash

ros2 launch robot_kernel robot_control_launch.py

👥 Contributors

    Hatim Ahmed Hassan - Lead Developer & Co-Founder (Beam Robotics) - Email

Acknowledgments

    Katapult Asia for the hardware and technical mentorship.

📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
