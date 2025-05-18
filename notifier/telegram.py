import requests

from rss_reader import settings


def send_message(text):
    url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': settings.CHAT_ID,
        'text': text,
        'disable_web_page_preview': False,
        'parse_mode': 'HTML'
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("✅ Message sent successfully")
    else:
        print("❌ Failed to send message")
        print(response.text)