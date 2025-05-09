# your_app/signals.py

import logging
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import ContactMessage, GoogleServiceAccount
from django.utils import timezone

logger = logging.getLogger(__name__)
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


def get_google_config():
    try:
        cfg = GoogleServiceAccount.objects.first()
        if not cfg or not cfg.credentials_file or not cfg.spreadsheet_id:
            raise Exception(
                "Chưa cấu hình GoogleServiceAccount (file JSON hoặc spreadsheet_id)."
            )
        with cfg.credentials_file.open("r") as f:
            info = json.load(f)
        return info, cfg.spreadsheet_id
    except Exception as e:
        logger.error(f"Lỗi load Google config từ DB: {e}")
        return None, None


@receiver(post_save, sender=ContactMessage)
def append_contact_to_sheet(sender, instance, created, **kwargs):
    if not created:
        return

    info, spreadsheet_id = get_google_config()
    if not info or not spreadsheet_id:
        return

    try:
        scope = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(info, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(spreadsheet_id).sheet1

        local_dt = timezone.localtime(instance.created_at)
        row = [
            local_dt.strftime("%Y-%m-%d"),
            local_dt.strftime("%H:%M"),
            instance.name,
            instance.phone_number,
            instance.message.replace("\n", " "),
        ]
        sheet.append_row(row, value_input_option="USER_ENTERED")
    except Exception as e:
        logger.error(
            f"Không thể append ContactMessage#{instance.id} vào Google Sheet: {e}"
        )
