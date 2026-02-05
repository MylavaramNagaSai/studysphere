from sqlalchemy.orm import Session
from fastapi import Depends
from app.models.user import User
from app.core.deps import get_db
from app.services.auth.password_service import hash_password
from app.services.auth.password_service import verify_password
from app.services.auth.jwt_service import create_access_token



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

@router.post("/set-password")
def set_password(
    email: str,
    password: str,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.is_email_verified:
        raise HTTPException(status_code=400, detail="Email not verified")

    user.hashed_password = hash_password(password)
    db.commit()

    return {"message": "Password set successfully"}
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.services.auth.otp_service import generate_otp, verify_otp
from app.services.auth.email_service import send_otp_email
from app.services.auth.password_service import hash_password
from app.core.deps import get_db
from app.models.user import User

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
def verify_email_otp(email: str, otp: str, db: Session = Depends(get_db)):
    if not verify_otp(email, otp):
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(email=email, is_email_verified=True)
        db.add(user)
    else:
        user.is_email_verified = True

    db.commit()
    return {"message": "Email verified successfully"}


@router.post("/set-password")
def set_password(
    email: str,
    password: str,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.is_email_verified:
        raise HTTPException(status_code=400, detail="Email not verified")

    user.hashed_password = hash_password(password)
    db.commit()

    return {"message": "Password set successfully"}
@router.post("/login")
def login(
    email: str,
    password: str,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not user.hashed_password:
        raise HTTPException(status_code=400, detail="Password not set")

    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": user.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
