**Chicken Feed Expert System**\
An expert system that recommends chicken feed based on type, age, and conditions. It has:

Backend (FastAPI) – rules engine and API

Frontend (Streamlit) – simple UI for interaction

**Setup**
1. Clone the repo
```bash
git clone https://github.com/morris-murigi/chicken-feed-expert-system.git
cd chicken-feed-expert-system
```
2. Install dependencies
```bash
pip install -r requirements.txt
```

**Run Locally**
Open two terminals in the project folder:

Terminal 1 → Start backend (API):
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
Terminal 2 → Start frontend (UI):
```bash
streamlit run app/ui/dashboard.py
```

API will run at 👉 http://localhost:8000

Streamlit UI at 👉 http://localhost:8501