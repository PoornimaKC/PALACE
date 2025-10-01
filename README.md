# PALACE – VR180 Video Processing App

PALACE is a FastAPI-based application designed to process and convert standard video files into **VR180-compatible format**.  
It provides a simple web interface where users can upload a video, process it, and download the converted result.

---

## 🚀 Features
- Upload video files via a web interface
- Process videos into VR180 format using FFmpeg + OpenCV
- Download processed results
- Built with **FastAPI**, **Uvicorn**, and **Jinja2 templates**
- Modular backend (`main.py`, `processing.py`) for easy extensions

---

## 📂 Project Structure
PALACE/
│
├── main.py # FastAPI entrypoint (routes, templates, API)
├── processing.py # Core video processing / ffmpeg logic
│
├── templates/
│ ├── index.html # Upload UI
│ └── status.html # Status / results page
│
├── requirements.txt # Python dependencies
├── start.sh # Start script for deployment (Render/production)
├── Dockerfile # Optional Docker build (ensures ffmpeg)
├── Procfile # Optional process definition
│
├── .gitignore # Ignores video files, cache, envs
└── README.md # Project documentation

---


## 🛠️ Setup (Local Development)

### 1. Clone Repo
```bash
git clone https://github.com/PoornimaKC/PALACE.git
cd PALACE

2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # (Linux/Mac)
venv\Scripts\activate      # (Windows)

3. Install Dependencies
```bash
pip install -r requirements.txt

4. Run App Locally
```bash
uvicorn main:app --reload
Visit: http://127.0.0.1:8000

⚡ Usage

1. Open the app in your browser.

2. Upload a supported video file.

3. The app will process it into VR180 format.

4. Download the processed video once completed.

✅ Requirements

* Python 3.9+ recommended

* FFmpeg installed (verify with ffmpeg -version)

* Tested on Windows + Linux

🔮 Further Improvements

 * Deploy on Render/Heroku and provide a public app link

 * Add progress bar / live status updates during processing

 * Support more VR formats (360, stereoscopic)

 * Cloud storage integration for large video files (AWS S3, GCS)

 * User authentication & history of conversions

 * Docker Compose setup for easier dev + deploy

📜 License

This project is for educational and experimental use.
Feel free to fork and extend for your own use cases.

 
