# Autonomous Indoor SLAM & YOLO Vision System

[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-EE4C2C?style=flat-square&logo=pytorch&logoColor=white)](https://pytorch.org/)
[![YOLOv8](https://img.shields.io/badge/YOLO-v8.0-00FFFF?style=flat-square)](https://github.com/ultralytics/ultralytics)
[![Flask](https://img.shields.io/badge/Flask-Web_Dashboard-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Arduino C++](https://img.shields.io/badge/Arduino-Firmware-00979D?style=flat-square&logo=arduino&logoColor=white)](https://www.arduino.cc/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

An end-to-end robotics software stack integrating real-time 2D indoor mapping (SLAM), closed-loop wheel odometry with IMU sensor fusion, YOLOv8 object detection, NCNN edge optimization for embedded hardware (Raspberry Pi), and a Flask telemetry web dashboard.

---

## Description

This project provides an integrated perception and localization solution for mobile indoor robots. By fusing wheel encoder feedback with 6-DOF IMU heading corrections, the system tracks real-time odometry and constructs statistical occupancy grid maps of indoor environments. Additionally, custom-trained YOLOv8 object detection models enable real-time detection of structural features (doors, windows, glass barriers) with low-latency edge deployment via NCNN on embedded computers such as the Raspberry Pi 3.

---

## Features

- **Real-Time 2D Indoor SLAM**: Occupancy grid mapping with raycasting sensor simulation and dynamic point-cloud map rendering.
- **Closed-Loop Robot Odometry**: Encoder tick counting combined with MPU6050 Gyro Z heading stabilization and PI speed control.
- **YOLOv8 Object Detection**: Custom vision pipeline trained to identify doors, windows, and glass elements in real-time streams.
- **Edge Hardware Acceleration**: Automated PyTorch (`.pt`) model conversion to FP16 NCNN format for high FPS execution on Raspberry Pi 3.
- **IP Camera & Local Web Stream**: Support for local webcams, smartphone IP video endpoints (IP Webcam app), and Raspberry Pi camera modules.
- **Flask Telemetry Dashboard**: Modern web interface displaying live video feed, detection log alerts, system metrics (FPS, CPU, RAM), and audio spectrum visualization.

---

## Technologies

- **Programming Languages**: Python 3.9+, C++ (Arduino)
- **Computer Vision & ML**: OpenCV, Ultralytics YOLOv8, PyTorch, NCNN
- **Mapping & Math**: NumPy, Matplotlib
- **Web Framework**: Flask, HTML5, Vanilla CSS3, JavaScript (ES6)
- **Hardware Integration**: Arduino Uno/Mega, MPU6050 IMU, Optical Wheel Encoders, Raspberry Pi 3

---

## Installation

### Prerequisites
- Python 3.9+
- Arduino IDE (for uploading microcontroller firmware)
- Git

### 1. Clone Repository
```bash
git clone https://github.com/username/autonomous-indoor-mapping-yolo-slam.git
cd autonomous-indoor-mapping-yolo-slam
```

### 2. Environment Setup
Create a virtual environment and install the required dependencies:

```bash
# Create virtual environment
python -m venv .venv

# Activate environment (Windows)
.venv\Scripts\activate

# Activate environment (Linux/macOS)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Usage

### 1. Microcontroller Firmware Setup
1. Open `odometry_code/odometry_code.ino` in Arduino IDE.
2. Select target board and COM port.
3. Upload sketch to the robot microcontroller.

### 2. Run Live SLAM Simulation
Simulate 2D room exploration and real-time mapping:
```bash
python indoor_mapping/live_slam_simulation.py
```

### 3. Display Saved Occupancy Map
Visualize final mapped boundaries from recorded scan logs:
```bash
python indoor_mapping/show_final_map.py
```

### 4. Run YOLO Object Detection

**Local Webcam:**
```bash
python model/detect.py
```

**IP Smartphone Camera:**
```bash
python model/detect_phone.py
```

**Raspberry Pi (NCNN Optimized):**
```bash
# 1. Export weights to NCNN format
python model/export_pi.py

# 2. Run detection on Pi
python model/detect_pi.py
```

### 5. Launch Telemetry Web Dashboard
```bash
python model/web_dashboard/app.py
```
Open `http://localhost:5000` in your web browser.

---

## Project Structure

```
autonomous-indoor-mapping-yolo-slam/
├── .env.example                      # Template environment configuration
├── .gitignore                        # Git exclusion rules
├── LICENSE                           # MIT License
├── README.md                         # Project documentation
├── requirements.txt                  # Python dependencies
├── indoor_mapping/                   # SLAM and mapping module
│   ├── arena_data.txt                # Sample spatial point-cloud data
│   ├── live_slam_simulation.py       # Interactive 2D SLAM simulation
│   ├── sample_sensor_data.txt        # Sample sensor measurement log
│   ├── show_final_map.py             # Occupancy map plotting script
│   └── legacy/                       # Archive mapping and motor routines
├── model/                            # YOLO Object Detection module
│   ├── best.pt                       # Trained PyTorch model weights
│   ├── detect.py                     # Local webcam inference script
│   ├── detect_phone.py               # IP camera inference script
│   ├── detect_pi.py                  # Raspberry Pi optimized inference script
│   ├── export_pi.py                  # NCNN conversion utility
│   ├── master_data.yaml              # Dataset configuration YAML
│   ├── setup_cpu.bat                 # Windows CPU setup helper
│   ├── setup_gpu.bat                 # Windows GPU setup helper
│   ├── start_training.bat            # Training launcher script
│   ├── train.py                      # YOLOv8 model training script
│   ├── yolov8n.pt                    # YOLOv8 nano pre-trained weights
│   ├── legacy_files/                 # Jupyter notebook and training history
│   └── web_dashboard/                # Flask web dashboard
│       ├── app.py                    # Flask server application
│       ├── static/                   # CSS and JavaScript assets
│       └── templates/                # HTML dashboard templates
└── odometry_code/                    # Microcontroller firmware
    └── odometry_code.ino             # Closed-loop motor control and IMU odometry
```

---

## Screenshots

> *Place project demonstration screenshots and dashboard GIFs here.*

| Live 2D SLAM Simulation | Flask Web Dashboard |
|---|---|
| *(SLAM Point Cloud Output)* | *(Real-Time Video Stream & Detection Logs)* |

---

## Future Improvements

- [ ] **ROS2 Integration**: Wrap odometry and sensor data into ROS2 nodes (`nav2` stack compatibility).
- [ ] **Extended Kalman Filter (EKF)**: Fuse IMU, wheel encoder ticks, and visual odometry.
- [ ] **Depth Vision**: Incorporate RGB-D camera point clouds for 3D mapping.
- [ ] **WebSockets Integration**: Replace HTTP polling in Flask web dashboard with Socket.IO streams.

---

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.
