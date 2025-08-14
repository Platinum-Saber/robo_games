# Robo Games

## Overview

This repository contains two distinct robotics projects:

- **Webots Simulation:** Virtual robot environments using the Webots simulator, allowing development and testing of robot algorithms in a controlled, physics-based simulation.
- **Kobuki Robot Implementation:** Real-world control code for the Kobuki mobile robot, run on a Raspberry Pi, with optional integration for a Kinect camera and OpenCV-based vision processing.

---

## 1. Webots Simulation

The Webots simulation provides a virtual environment for robotics development. It does **not** directly simulate the Kobuki robot hardware or its Raspberry Pi code, but rather offers a general-purpose robotics playground.

- **Features:**
  - 3D visualization and physics
  - Custom robot models and worlds
  - Useful for rapid prototyping and algorithm testing

- **Getting Started:**
  - Install Webots: [Download](https://cyberbotics.com/#download)
  - Instructions and sample worlds are typically located in the `webots/` directory.
  - Refer to the [Webots documentation](https://cyberbotics.com/doc/guide/index) for more details.

---

## 2. Kobuki Robot Implementation

The Kobuki robot code is intended for deployment on real hardware, specifically the Kobuki base with a Raspberry Pi. This code is **separate** from the Webots simulation.

- **Location:** See the `kobuki/` folder.
- **Description:**  
  > This folder contains the Raspberry Pi codes for Kobuki

- **Typical Features:**
  - Real-time control of the Kobuki robot’s motors and sensors
  - Integration with a Kinect camera for RGB and depth perception
  - Image processing using OpenCV for tasks such as object detection, navigation, and obstacle avoidance

- **Getting Started:**
  - Deploy the code to your Raspberry Pi connected to Kobuki.
  - Ensure all dependencies (e.g., OpenCV, camera drivers) are installed.
  - Refer to any provided scripts or documentation in the `kobuki/` folder.

---

## Notes on Kinect and OpenCV

- Kinect camera integration provides streaming RGB and depth data.
- OpenCV is used for real-time image analysis and robotics vision tasks.
- This functionality is only present in the Kobuki robot implementation (not the Webots simulation).

---

## Directory Structure

```
robo_games/
├── webots/              # Webots simulation worlds and configuration
├── kobuki/              # Real robot implementation for Kobuki + Raspberry Pi (+ Kinect + OpenCV)
├── README.md            # This file
└── ...
```

---

## Additional Resources

- [Webots Documentation](https://cyberbotics.com/doc/guide/index)
- [Kobuki Documentation](https://kobuki.readthedocs.io/_/downloads/en/stable/pdf/)
- [OpenCV Documentation](https://opencv.org/)

---

## Contributing

Contributions for both simulation and real-robot code are welcome! Please open issues or pull requests with suggestions or improvements.

---

## License

This project is licensed under the MIT License.

---

