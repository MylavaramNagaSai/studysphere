from fastapi import FastAPI

app = FastAPI(
    title="StudySphere Backend",
    version="0.1.0"
)

@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "StudySphere backend is running 🚀"
    }
