# 🤖 Autonomous Security Robot (Sherlock Robot)

[![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Dashboard-black?logo=flask)](https://flask.palletsprojects.com/)
[![YOLO](https://img.shields.io/badge/YOLO-Detection-red?logo=pytorch)](https://pjreddie.com/darknet/yolo/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![Status](https://img.shields.io/badge/Status-Development-orange)]()

---

## 📖 Overview

The **Autonomous Security Robot (Sherlock)** is a **ROS-inspired surveillance system** designed for **patrolling, object detection, and real-time monitoring**.  
This project integrates **Python-based control**, **YOLO object detection**, and a **Flask-powered dashboard** to create a modular, real-world-ready security robot.

It can autonomously **navigate**, **detect intruders**, and **log alerts** for later analysis.  

---

## 🎯 Key Features

- **Real-Time Object Detection** using **YOLO** models for intruder and anomaly detection.
- **Autonomous Navigation** with planned patrol routes and obstacle avoidance (future expansion).
- **Surveillance Dashboard** built with Flask for real-time video streaming and alert management.
- **Alert System** – Automatic image capture & storage in `alert_images/` with timestamps.
- **Database Integration** for logs and alert storage.
- **Modular Architecture** – Easy to expand with additional sensors or AI models.

---

## 🧰 Tech Stack

- **Programming:** Python 3.10  
- **Computer Vision:** OpenCV, YOLO  
- **Web Framework:** Flask (Dashboard)  
- **Database:** SQLite (for logging alerts)  
- **Hardware:** Raspberry Pi / ESP32 (for robot control & sensors)  

---

## 🗂 Project Structure

```

Sherlock\_Robot\_v0.x/
│
├── Models/                     # YOLO models for detection
├── alert\_images/               # Captured intruder images
├── database/                   # SQLite database files
├── src/                        # Core robot logic & CV modules
├── static/                     # Dashboard static assets (CSS, JS, etc.)
├── templates/                  # Flask HTML templates
├── tools/                      # Utility scripts & tools
├── surveillance-robot-dashboard/  # Dashboard module
├── main.py                     # Main application entry point
├── tester.py                   # Testing script for modules
├── packages.txt                # Required Python packages
└── README.md

````

---

## ⚙️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/xaatim/Autonomous-Security-Robot.git
   cd Autonomous-Security-Robot
````

2. **Create a virtual environment & install dependencies**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   pip install -r packages.txt
   ```

3. **Run the main script**

   ```bash
   python main.py
   ```

4. **Access the dashboard**
   Open your browser and navigate to:

   ```
   http://localhost:5000
   ```

---

## 📷 Visuals

All **rendered dashboards**, **intruder alert samples**, and **engineering drawings** are located in the [`alert_images/`](./alert_images/) and [`static/`](./static/) folders.

---

## 🚀 Future Improvements

* **ROS2 Integration** for advanced robot navigation.
* **Automated Charging Dock** for continuous operation.
* **Advanced Intrusion Analytics** with deep learning.
* **Integration with IoT (MQTT/Blynk)** for remote alerts.

---

## 📄 License

This project is licensed under the **MIT License**. See [`LICENSE`](./LICENSE) for details.

---

## 👤 Author

**Hatim Ahmed Hassan** – 2025
For inquiries or collaborations: **[xayari229@gmail.com](mailto:xayari229@gmail.com)**

