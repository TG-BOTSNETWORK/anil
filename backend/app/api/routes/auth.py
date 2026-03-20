from fastapi import APIRouter, Depends, Response, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
import re

from app.db.session import get_db
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter()


# -------------------------------
# ✅ SCHEMAS
# -------------------------------
class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    whatsapp_number: str  # ✅ Mandatory


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# -------------------------------
# ✅ SIGNUP
# -------------------------------
@router.post("/signup")
def signup(data: SignupRequest, db: Session = Depends(get_db)):

    # 1️⃣ Check if user already exists
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    # 2️⃣ Clean + Validate WhatsApp number
    whatsapp_number = re.sub(r"\s|-", "", data.whatsapp_number)

    if not whatsapp_number.startswith("+"):
        whatsapp_number = "+91" + whatsapp_number

    if not re.match(r"^\+91\d{10}$", whatsapp_number):
        raise HTTPException(
            status_code=400,
            detail="Invalid Indian WhatsApp number format"
        )

    # 3️⃣ Create user
    user = User(
        email=data.email,
        name=data.email.split("@")[0],
        password=hash_password(data.password),
        whatsapp_number=whatsapp_number
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "msg": "User created successfully",
        "user": {
            "id": user.id,
            "email": user.email,
            "whatsapp_number": user.whatsapp_number
        }
    }


# -------------------------------
# ✅ LOGIN
# -------------------------------
@router.post("/login")
def login(data: LoginRequest, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"user_id": user.id})

    # ✅ Set cookie properly for frontend
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,     # 🔒 True in production (HTTPS)
        samesite="lax",   # ✅ required for frontend requests
        path="/",         # ✅ IMPORTANT (fixes cookie issues)
        max_age=60 * 60 * 24 * 7
    )

    return {
        "msg": "Login successful",
        "user": {
            "id": user.id,
            "email": user.email,
            "whatsapp_number": user.whatsapp_number
        }
    }


# -------------------------------
# ✅ LOGOUT
# -------------------------------
@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        path="/"   # ✅ IMPORTANT
    )
    return {"msg": "Logged out successfully"}