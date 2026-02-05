import random
import time

# In-memory OTP store (TEMP – for development)
otp_store = {}

OTP_EXPIRY_SECONDS = 300  # 5 minutes


def generate_otp(email: str) -> str:
    otp = str(random.randint(100000, 999999))
    otp_store[email] = {
        "otp": otp,
        "expires_at": time.time() + OTP_EXPIRY_SECONDS
    }
    print(f"[StudySphere OTP] Email: {email}, OTP: {otp}")
    return otp


def verify_otp(email: str, otp: str) -> bool:
    record = otp_store.get(email)

    if not record:
        return False

    if time.time() > record["expires_at"]:
        del otp_store[email]
        return False

    if record["otp"] != otp:
        return False

    del otp_store[email]
    return True
