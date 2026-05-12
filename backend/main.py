from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "MDIP backend running on GitHub"}