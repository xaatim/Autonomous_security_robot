# Autonomous Indoor Surveillance Robot (SCUTTLE-Intel AMR)
![ROS2](https://img.shields.io/badge/ros2-humble-blue?logo=ros&logoColor=white)
![Python](https://img.shields.io/badge/python-3.10-blue?logo=python&logoColor=white)
![C++](https://img.shields.io/badge/c++-14%2F17-blue?logo=c%2B%2B&logoColor=white)
![Ubuntu](https://img.shields.io/badge/Ubuntu-22.04_LTS-orange?logo=ubuntu&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Intel_AMR-0071C5?logo=intel&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Container-2496ED?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

A fully autonomous mobile security unit featuring LiDAR SLAM, biometric intruder detection, and cloud-native fleet integration.

## Strategic Collaboration

<a href="https://katapultasia.com/">
<img src="https://katapultasia.com/wp-content/uploads/2020/06/katapult-logo.png" height="50" alt="Katapult Asia">
</a>

This project was developed in collaboration with **Katapult Asia (Malaysia)**, who provided the SCUTTLE-Intel AMR hardware platform and technical mentorship to enable real-world validation.

## Project Overview

This project implements a modular indoor surveillance system on the SCUTTLE-Intel Autonomous Mobile Robot (AMR). Unlike traditional passive CCTV systems, this robot is designed to:

* **Autonomously Patrol:** Navigates indoor environments without human intervention.
* **Dynamic Mapping:** Builds and updates maps using SLAM (Simultaneous Localization and Mapping).
* **Active Intruder Detection:** Identifies unauthorized individuals using edge-computed deep learning.

The system is built on **ROS 2 Humble** and integrates the Nav2 Stack for navigation, InsightFace for real-time recognition, and a Store-First Protocol to secure forensic evidence locally before cloud transmission.

---

## Beam Robotics Integration

This autonomous unit serves as the hardware flagship for **Beam Robotics**, a co-founded initiative focused on secure, scalable robotic deployments with integrated monitoring dashboards. Each robot pairs with the Beam Robotics cloud infrastructure, providing encrypted access per device owner.

### 1. The Beam Platform
The central hub for Beam Robotics products manages the ecosystem of deployed robots and provides a unified entry point for hardware control and monitoring.

![Beam Robotics Landing Page](docs/product_showcase/beam_homepage.png)

### 2. Fleet Management & Robot Selection
After authentication, customers access a private fleet interface showing only robots registered to their specific account.
* **Exclusive Access:** Only the verified owner can access the robot dashboard.
* **Robot Registration:** Devices are added using a unique cryptographic key.
* **Customization:** Configuration of robot-specific add-ons (GPS, sensors, modules).

![Fleet Selection Interface](docs/product_showcase/beam_fleet_view.png)

### 3. Live Command Dashboard
Selecting a robot opens its dedicated command center, featuring encrypted low-latency video feeds and real-time telemetry.

![Client Dashboard UI](docs/product_showcase/client_dashboard_ui.png)

---

## Computer Vision Performance

Our proprietary vision pipeline is optimized for real-world unpredictability and exceeds standard academic baselines.

### 1. Robustness to Environment
The system maintains high accuracy in low-light environments (<50 lux) and performs reliably under direct sunlight and harsh indoor lighting.

![Environmental Robustness](docs/product_showcase/environmental_robustness.png)

### 2. Advanced Occlusion Handling
The system detects and flags risks even when faces are partially occluded (e.g., masks) by utilizing facial geometry analysis rather than simple texture matching.

![Occlusion Analysis](docs/product_showcase/occlusion_analysis.png)

### 3. Tuning & Accuracy
Validated on 200 real inference trials, the system achieved a **0% False Acceptance Rate (FAR)** at the optimal threshold.

![Performance Metrics](docs/product_showcase/performance_metrics.png)

---

## Technical Specifications

### Autonomous Navigation
* **SLAM:** 2D occupancy grid generation using SLAM Toolbox.
* **Path Planning:** Nav2 (Behavior Trees) for dynamic obstacle avoidance.
* **Localization:** AMCL with ±5 cm pose accuracy.

### Intelligent Perception
* **Face Recognition:** InsightFace + Cosine Similarity scoring.
* **Alert System:** Captures images of unknown individuals, stores evidence locally (store-first protocol), and transmits automated email alerts.

### Hardware Control
* **Drive System:** Custom ROS 2 hardware interface (differential drive).
* **Latency Optimization:** Non-blocking surveillance threads achieving ~110 ms average system latency.

### Tech Stack & Hardware Components

| Category | Component |
| :--- | :--- |
| **Compute** | Axiomtek Embedded Computer (Intel Architecture) |
| **Chassis** | SCUTTLE-Intel AMR Kit (Differential Drive) |
| **LiDAR** | YDLIDAR X2 / X4 (2D scanning) |
| **Vision** | Intel RealSense D435i (RGB-D) |
| **Actuators** | Cytron DC Motors, MD10C Motor Drivers |
| **OS** | Ubuntu 22.04 LTS (Jammy Jellyfish) |
| **Middleware** | ROS 2 Humble Hawksbill |
| **Languages** | Python 3.10, C++ |

---

## Repository Structure

```text
Autonomous-Security-Robot/
├── src/
│   ├── robot_kernel/          # Socket.IO client & Dashboard connectivity
│   ├── robot_vision/          # InsightFace logic, camera nodes, alerting
│   ├── generic_robot_driver/  # URDF models, hardware interfaces, params
│   └── ydlidar_ros2_driver/   # LiDAR sensor drivers
├── docs/
│   └── product_showcase/      # Product results & Beam platform screenshots
├── maps/                      # Saved SLAM maps (.yaml / .pgm)
├── docker/                    # Docker containers for deployment
└── README.md

```

## Installation

### 1. Prerequisites

* Ubuntu 22.04
* ROS 2 Humble installed and sourced

### 2. Setup Workspace

```bash
mkdir -p ~/scuttle_ws/src
cd ~/scuttle_ws/src
git clone [https://github.com/xaatim/Autonomous-Security-Robot.git](https://github.com/xaatim/Autonomous-Security-Robot.git) .

```

### 3. Install Dependencies

```bash
cd ~/scuttle_ws
rosdep update
rosdep install --from-paths src --ignore-src -r -y
pip install -r src/Autonomous_security_robot-myFyp-/requirements.txt

```

### 4. Build

```bash
colcon build --symlink-install
source install/setup.bash

```

## Usage

### 1. Launch Robot (Hardware & Drivers)

```bash
ros2 launch generic_robot_driver scuttle_full.launch.py

```

### 2. Start Surveillance & Navigation

```bash
ros2 launch robot_kernel robot_control_launch.py

```

## Contributors

**Hatim Ahmed Hassan**

* Lead Developer & Co-Founder (Beam Robotics)
* **Email:** xayari229@gmail.com

## Acknowledgments

Special thanks to **Katapult Asia** for providing hardware support and technical mentorship.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
