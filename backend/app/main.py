from fastapi import FastAPI
from app.api.auth.routes import router as auth_router
from app.core.database import engine, Base

# 👇 IMPORT MODELS HERE (CRITICAL)
from app.models import user  

app = FastAPI(
    title="StudySphere Backend",
    version="0.1.0"
)

# 👇 NOW SQLAlchemy KNOWS ABOUT User
Base.metadata.create_all(bind=engine)

app.include_router(auth_router)

@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "StudySphere backend is running 🚀"
    }
