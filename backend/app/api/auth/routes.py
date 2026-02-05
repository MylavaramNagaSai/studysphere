from fastapi import APIRouter, HTTPException
from app.services.auth.otp_service import generate_otp, verify_otp
from app.services.auth.email_service import send_otp_email

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.get("/health")
def auth_health():
    return {"auth": "ok"}

@router.post("/email/send-otp")
async def send_email_otp(email: str):
    otp = generate_otp(email)
    await send_otp_email(email, otp)
    return {"message": "OTP sent to email"}

@router.post("/email/verify-otp")
def verify_email_otp(email: str, otp: str):
    if verify_otp(email, otp):
        return {"message": "Email verified successfully"}
    raise HTTPException(status_code=400, detail="Invalid or expired OTP")
