import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

# ─────────────────────────────────────────────
# 📌 Helper: Prepare Content
# ─────────────────────────────────────────────
def prepare_content(news):
    return f"""
📰 {news.title}

{news.ai_summary or news.summary}

🔗 Read more: {news.url}
"""


# ─────────────────────────────────────────────
# 📧 EMAIL SERVICE
# ─────────────────────────────────────────────
def send_email(content, to_email):
    try:
        if not to_email:
            raise ValueError("No recipient email provided")

        msg = MIMEText(content, "plain", "utf-8")
        msg["Subject"] = "🚀 AI News Update"
        msg["From"] = os.getenv("EMAIL_USER")
        msg["To"] = to_email

        with smtplib.SMTP(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT"))) as server:
            server.starttls()
            server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
            server.send_message(msg)

        print(f"✅ EMAIL SENT → {to_email}")
        return {"status": "sent"}

    except Exception as e:
        print("❌ EMAIL ERROR:", e)
        return {"status": "failed", "error": str(e)}


# ─────────────────────────────────────────────
# 📱 WHATSAPP SERVICE (Twilio)
# ─────────────────────────────────────────────
def send_whatsapp(content, to_number):
    try:
        if not to_number:
            raise ValueError("No WhatsApp number provided")

        # ensure correct format
        if not to_number.startswith("whatsapp:"):
            to_number = f"whatsapp:{to_number}"

        client = Client(
            os.getenv("TWILIO_SID"),
            os.getenv("TWILIO_AUTH_TOKEN")
        )

        message = client.messages.create(
            body=content[:1500],  # Twilio limit safety
            from_=os.getenv("TWILIO_WHATSAPP_NUMBER"),
            to=to_number
        )

        print(f"✅ WHATSAPP SENT → {to_number}")
        return {"status": "sent", "sid": message.sid}

    except Exception as e:
        print("❌ WHATSAPP ERROR:", e)
        return {"status": "failed", "error": str(e)}


# ─────────────────────────────────────────────
# 📢 OTHER CHANNELS (Mock / Extend later)
# ─────────────────────────────────────────────
def post_linkedin(content):
    print("🔗 [LINKEDIN POST]", content)


def publish_blog(content):
    print("📝 [BLOG]", content)


def send_newsletter(content):
    print("📧 [NEWSLETTER]", content)


# ─────────────────────────────────────────────
# 🚀 MAIN BROADCAST FUNCTION
# ─────────────────────────────────────────────
def broadcast_news(news, channels, user):
    """
    user → current logged-in user
    expects:
        user.email
        user.whatsapp_number
    """

    content = prepare_content(news)
    results = []

    for ch in channels:

        # 📧 EMAIL
        if ch == "email":
            res = send_email(content, user.email)
            results.append({"channel": "email", **res})

        # 📱 WHATSAPP
        elif ch == "whatsapp":
            res = send_whatsapp(content, user.whatsapp_number)
            results.append({"channel": "whatsapp", **res})

        # 🔗 LINKEDIN (mock)
        elif ch == "linkedin":
            post_linkedin(content)
            results.append({"channel": "linkedin", "status": "mocked"})

        # 📝 BLOG (mock)
        elif ch == "blog":
            publish_blog(content)
            results.append({"channel": "blog", "status": "mocked"})

        # 📧 NEWSLETTER (mock)
        elif ch == "newsletter":
            send_newsletter(content)
            results.append({"channel": "newsletter", "status": "mocked"})

        else:
            results.append({"channel": ch, "status": "invalid"})

    return results