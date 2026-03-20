import os
from dotenv import load_dotenv

load_dotenv()  # Load local .env

class Settings:
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    # Anthropic API
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY")

    # Email
    SMTP_SERVER: str = os.getenv("SMTP_SERVER")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 587))
    EMAIL_USER: str = os.getenv("EMAIL_USER")
    EMAIL_PASS: str = os.getenv("EMAIL_PASS")

    # Twilio (WhatsApp)
    TWILIO_SID: str = os.getenv("TWILIO_SID")
    TWILIO_AUTH_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_WHATSAPP_NUMBER: str = os.getenv("TWILIO_WHATSAPP_NUMBER")

settings = Settings()