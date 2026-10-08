# 🍅 Personal Pomodoro & Focus Dashboard

A modern, distraction-free **Personal Pomodoro & Focus Dashboard** built with **Python 3.12** and **Streamlit**.

---

## ✨ Features

- **25-Minute Pomodoro Countdown**: Standard Pomodoro focus interval with Start, Pause, and Reset controls.
- **Visual Progress Bar**: Real-time progress bar with live completion percentage and remaining time calculation.
- **Interactive Ambient Focus Audio**: Selection dropdown with instant ambient atmosphere embeds:
  - 🌧️ Heavy Rain
  - ☕ Cozy Café
  - 🌲 Peaceful Forest
  - 📻 White Noise
  - 🔇 Silence (Mute)
- **Session & Deep Work Tracking**: Automatically tracks completed sessions and cumulative deep work minutes.
- **Focus Goal Tracker**: Quick task input to keep your focus objective front-and-center.
- **Clean Responsive Dark-Themed UI**: Polished dashboard aesthetic optimized for focus.

---

## 🚀 Quick Start (Local Run)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Streamlit Application
```bash
streamlit run app.py
```
After running this command, open your browser and navigate to:
```
http://localhost:8501
```

---

## 🧪 Running Unit Tests
Unit tests are written with `pytest` to verify timer logic, edge cases, and time formatting:
```bash
pytest test_app.py
```

---

## 🐳 Running with Docker

### 1. Build the Docker Image
```bash
docker build -t pomodoro-dashboard .
```

### 2. Run the Container
```bash
docker run -p 8501:8501 pomodoro-dashboard
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📁 Project Structure

```
├── app.py              # Main Streamlit web application & timer logic
├── test_app.py         # Pytest unit tests for timer calculations
├── requirements.txt    # Application dependencies (streamlit, pytest)
├── Dockerfile          # Container configuration for Python 3.12
├── .gitignore          # Git ignore rules for Python artifacts
└── README.md           # Project documentation & run guide
```
