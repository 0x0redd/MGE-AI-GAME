<p align="center">
  <img src="https-your-path-here/asteroid-sprint-banner.png" alt="Asteroid Sprint Banner" width="800"/>
</p>

<h1 align="center">Asteroid Sprint</h1>

<p align="center">
  <strong>Navigate a deadly asteroid field using only your hands!</strong>
  <br />
  A unique, controller-free gaming experience powered by computer vision and keypoint detection.
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-GPL_3.0-blue.svg" alt="License"></a>
  <img src="https://img.shields.io/badge/Python-3.9+-brightgreen.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Built_with-PygameCE-orange.svg" alt="PygameCE">
  <img src="https://img.shields.io/badge/Controls-Hand_Gestures-informational.svg" alt="Hand Gestures">
</p>

> **Proudly showcased at the Moroccan Gaming Expo!** This project was developed by the **Computer Science Club** at **Moulay Ismail University** to demonstrate the future of interactive, AI-driven entertainment.

<br>

<p align="center">
  <img src="https-your-path-here/gameplay-demo.gif" alt="Asteroid Sprint Gameplay" width="700"/>
</p>

## ✨ Features

*   **Controller-Free Gameplay:** Use your hand gestures to intuitively control the spaceship.
*   **AI-Powered Controls:** Leverages real-time keypoint detection to track your hand movements.
*   **Endless Survival:** Dodge an ever-increasing barrage of asteroids and compete for the high score.
*   **Dynamic VFX:** Features custom-made particle effects for the ship's thrusters and explosive deaths.
*   **Engaging Audio:** Includes thematic music and sound effects to enhance the experience.

## 🚀 Getting Started

Follow these steps to get the game up and running on your local machine.

### Prerequisites

*   [Python 3.9+](https://www.python.org/downloads/)
*   A webcam for hand gesture detection.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/asteroid-sprint.git
    cd asteroid-sprint
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install the required packages:**
    ⚠️ **Important:** If you have the standard `pygame` library installed, you must uninstall it first to use `pygame-ce`.
    ```bash
    pip uninstall pygame
    pip install pygame-ce opencv-python mediapipe
    ```
    *(Note: Added opencv and mediapipe, which are typically required for keypoint detection.)*

## 🎮 How to Play

1.  **Launch the game:**
    ```bash
    python asteroid_sprint.py
    ```
2.  **Position yourself** so your webcam can clearly see your hand.
3.  Use your **hand movements** to control the ship and dodge the falling asteroids. Survive as long as you can!

## 🤝 Contributing

We welcome all feedback, suggestions, and contributions! This project is a product of our passion for technology and gaming, and we believe in the power of community.

If you encounter any issues or have ideas for improvement, please **create an issue** in this repository.

## 🌟 Credits & Acknowledgements

This game was made possible by the passion and dedication of the **Computer Science Club** at **Moulay Ismail University**.

*   **Spaceship Fire Trail:** Customized from [pygame-vfx](https://github.com/kadir014/pygame-vfx) by @kadir014.
*   **Death Particles:** Customized from [vfx](https://github.com/eliczi/vfx) by @eliczi.
*   **Font:** [Orbitron](https://www.theleagueofmoveabletype.com/orbitron) by The League of Moveable Type.
*   **Music:** "Screen Saver" by Kevin MacLeod ([incompetech.com](https://incompetech.com)).

All licenses for third-party assets are available in the `licenses` folder.

## 📄 License

This project is licensed under the **GPL-3.0 License**. See the `LICENSE` file for more details.