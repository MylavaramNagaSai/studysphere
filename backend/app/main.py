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
from fastapi import FastAPI
from app.api.auth.routes import router as auth_router

app = FastAPI(
    title="StudySphere Backend",
    version="0.1.0"
)

app.include_router(auth_router)

@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "StudySphere backend is running 🚀"
    }
