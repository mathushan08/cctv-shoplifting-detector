# 🛒 CCTV Shoplifting Detector

A computer vision project to detect suspicious activities such as loitering, picking, and concealing items using CCTV/webcam footage.  
Built with **Python**, **OpenCV**, **YOLOv8**, and **DeepSORT**.

---

## 📌 Features
- Real-time object detection using YOLOv8  
- Person tracking with DeepSORT  
- Customizable zones (e.g., shelf zone, exit zone)  
- Alerts for suspicious activity (loitering, conceal, pick events)  
- Webcam or CCTV feed support  

---

## ⚡ Requirements
- Python **3.9+**
- Git
- Webcam (for testing) or CCTV RTSP feed

---

## 🖥️ Setup Instructions

### 🔹 1. Clone the Repository
```bash
git clone https://github.com/your-username/cctv-shoplifting-detector.git
cd cctv-shoplifting-detector
```

---

### 🔹 2. Create a Virtual Environment

#### On **Windows (Command Prompt)**
```bash
python -m venv venv
venv\Scripts\activate
```

#### On **macOS / Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 🔹 3. Install Dependencies
```bash
pip install -r requirements.txt
```

If `requirements.txt` is not available yet, you can generate it from your current environment:
```bash
pip freeze > requirements.txt
```

---

### 🔹 4. Run the Program
```bash
python main.py
```

- Default mode: runs on webcam
- To test on a video file:
```bash
python main.py --source path/to/video.mp4
```

---

## ⚙️ Configuration

- **Zones**: The app allows you to define shelf zones and exit zones by clicking on the video feed.  
- **Loitering time**: Default is 10 seconds (configurable inside `main.py`).  
- **Alerts**: Currently logged in the console, can be extended to email/Telegram.

---

## 🧪 Development Workflow
- Work on a **feature branch** (e.g., `dev`)  
- Push changes:
```bash
git add .
git commit -m "Added new feature"
git push origin dev
```
- Create a Pull Request on GitHub for review  

---

## 📦 Useful Commands

- Update dependencies:
```bash
pip install -r requirements.txt --upgrade
```

- Deactivate virtual environment:
```bash
deactivate
```

---

## 🚀 Roadmap
- [ ] Improve conceal detection logic  
- [ ] Add real item detection (e.g., bottles, snacks)  
- [ ] Save alert video clips automatically  
- [ ] Integrate alert system (Email/Telegram/Slack)  

---

## 👥 Contributing
1. Fork the repo  
2. Create a feature branch (`git checkout -b feature-name`)  
3. Commit changes (`git commit -m "Added feature"`)  
4. Push branch (`git push origin feature-name`)  
5. Open a Pull Request  

---

## ⚖️ Disclaimer
This project is for **educational purposes only**.  
It should not be used as the sole method of security or surveillance in real-world stores.  
