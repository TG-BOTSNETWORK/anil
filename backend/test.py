# whatsapp_broadcast_selenium.py
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# ───────── CONFIG ─────────
# Example users with WhatsApp numbers (replace with your DB fetch)
users = [
    { "whatsapp_number": "9392832240"},
    {"whatsapp_number": "6305101934"},
]

# Example news object
class News:
    def __init__(self, title, summary, url, ai_summary=None):
        self.title = title
        self.summary = summary
        self.ai_summary = ai_summary
        self.url = url

news_item = News(
    title="AI Breaking News!",
    summary="This is a sample news summary.",
    ai_summary="AI-generated summary for quick reading.",
    url="https://example.com/news/123"
)

# ───────── HELPER: PREPARE MESSAGE ─────────
def prepare_content(news):
    return f"""
📰 {news.title}

{news.ai_summary or news.summary}

🔗 Read more: {news.url}
"""

# ───────── SETUP CHROME DRIVER ─────────
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get("https://web.whatsapp.com/")

print("Scan QR code if not already logged in...")
time.sleep(15)  # Give time to scan

# ───────── SEND WHATSAPP MESSAGE ─────────
def send_whatsapp_message(number, message):
    try:
        # Ensure Indian format
        if not number.startswith("+"):
            number = "+91" + number
        to_number = f"whatsapp:{number}"

        # Search contact
        search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
        search_box.clear()
        search_box.send_keys(number)
        search_box.send_keys(Keys.ENTER)
        time.sleep(2)  # wait for chat to open

        # Type and send message
        message_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
        message_box.click()
        message_box.send_keys(message)
        message_box.send_keys(Keys.ENTER)

        print(f"✅ WHATSAPP SENT → {to_number}")
    except Exception as e:
        print(f"❌ WHATSAPP ERROR → {number}: {e}")

# ───────── BROADCAST TO ALL USERS ─────────
content = prepare_content(news_item)

for user in users:
    if user.get("whatsapp_number"):
        send_whatsapp_message(user["whatsapp_number"], content)
        time.sleep(1)  # small delay to avoid UI issues

driver.quit()
print("✅ All WhatsApp messages sent!")