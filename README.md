### Running the Program
```bash
pip install -r requirements.txt
```
#### Locally
```bash
uvicorn app.main:app --reload
```
#### Render
```bash
web: uvicorn app.main:app --host 0.0.0.0 --port 10000
```