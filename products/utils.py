import requests
from django.core.mail import send_mail
from django.conf import settings


def send_order_notifications(order):
    """
    Sends Email and Telegram notifications for a new order.
    """
    # 1. Construct the message
    variant_info = f"{
        order.variant.volume.name}" if order.variant else "No specific volume selected"
    message = (
        f"📦 NEW ORDER RECEIVED\n\n"
        f"Product: {order.product.name}\n"
        f"Variant: {variant_info}\n"
        f"Qty: {order.quantity}\n\n"
        f"👤 Customer: {order.first_name} {order.last_name}\n"
        f"📞 Phone: {order.phone}\n"
        f"📧 Email: {order.email or 'N/A'}\n"
        f"📝 Remarks: {order.remarks or 'None'}"
    )

    # 2. Send Email (Admin)
    try:
        send_mail(
            subject=f"New Order: {order.product.name}",
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            # Add ADMIN_EMAIL to settings.py
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=True,
        )
    except Exception as e:
        print(f"Error sending email: {e}")

    # 3. Send Telegram Notification
    # Add TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID to settings.py
    if hasattr(settings, 'TELEGRAM_BOT_TOKEN') and hasattr(settings, 'TELEGRAM_CHAT_ID'):
        telegram_url = f"[https://api.telegram.org/bot](https://api.telegram.org/bot){
            settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": settings.TELEGRAM_CHAT_ID,
            "text": message
        }
        try:
            requests.post(telegram_url, data=payload, timeout=5)
        except Exception as e:
            print(f"Error sending Telegram: {e}")
