from dotenv import load_dotenv
load_dotenv()   # 👈 THIS MUST BE HERE

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
import os

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

async def send_otp_email(email: EmailStr, otp: str):
    message = MessageSchema(
        subject="StudySphere – Email Verification OTP",
        recipients=[email],
        body=f"""
Hello 👋

Your StudySphere verification OTP is:

🔐 {otp}

This OTP is valid for 5 minutes.

If you did not request this, please ignore this email.

— StudySphere Team
""",
        subtype="plain"
    )

    fm = FastMail(conf)
    await fm.send_message(message)
