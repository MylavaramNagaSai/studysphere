from fastapi import APIRouter, HTTPException
from app.services.auth.otp_service import generate_otp, verify_otp

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/health")
def auth_health():
    return {"auth": "ok"}


@router.post("/email/send-otp")
def send_email_otp(email: str):
    generate_otp(email)
    return {"message": "OTP sent to email"}


@router.post("/email/verify-otp")
def verify_email_otp(email: str, otp: str):
    if verify_otp(email, otp):
        return {"message": "Email verified successfully"}
    raise HTTPException(status_code=400, detail="Invalid or expired OTP")
