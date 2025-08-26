### Running the Program
```bash
pip install -r requirements.txt
```
#### Locally
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
streamlit run app/ui/dashboard.py
```
#### Render
```bash
web: uvicorn app.main:app --host 0.0.0.0 --port 10000
```
```bash
# Linux / Mac
source .venv/bin/activate  

# Windows CMD
.venv\Scripts\Activate.bat
pip show streamlit
pip show requests
```

Explanations