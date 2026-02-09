import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def send_telegram_message(message):
    """
    Sends a message to the configured Telegram group.
    """
    try:
        # Ensure these are set in your settings.py
        token = settings.TELEGRAM_BOT_TOKEN
        chat_id = settings.TELEGRAM_CHAT_ID

        if not token or not chat_id:
            logger.warning(
                "Telegram settings not configured. Message skipped.")
            return

        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML"  # Optional: allows bold/italic in messages
        }

        response = requests.post(url, data=payload, timeout=10)
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send Telegram message: {e}")
