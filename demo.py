from fastapi import FastAPI

app = FastAPI()

@app.get("/status")
def root():
    return {
        "status": "OK"
    }
