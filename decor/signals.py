# your_app/signals.py

import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import ContactMessage
from django.utils import timezone

# Đường dẫn tới JSON key

# ID của Google Sheet (phần giữa "/d/" và "/edit" trong URL)
SPREADSHEET_ID = "1noay5wYR89Y3WuSSwcDRPhZxKG0g6EAL-1QVMh5q00c"

# Thiết lập kết nối
scope = ["https://www.googleapis.com/auth/spreadsheets"]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    settings.CREDENTIALS_FILE, scope
)
gc = gspread.authorize(creds)

sheet = gc.open_by_key(SPREADSHEET_ID).sheet1  # hoặc .worksheet('Tên sheet')


@receiver(post_save, sender=ContactMessage)
def append_contact_to_sheet(sender, instance, created, **kwargs):
    if not created:
        return
    # Tạo một hàng mới dựa trên instance
    local_dt = timezone.localtime(instance.created_at)
    row = [
        local_dt.strftime("%Y-%m-%d"),
        local_dt.strftime("%H:%M"),
        instance.name,
        instance.phone_number,
        instance.message.replace("\n", " "),
    ]
    try:
        sheet.append_row(row, value_input_option="USER_ENTERED")
    except Exception as e:
        # Xử lý lỗi (gửi mail, log, ...)
        import logging

        logger = logging.getLogger(__name__)
        logger.error(
            f"Không thể append ContactMessage#{instance.id} vào Google Sheet: {e}"
        )
