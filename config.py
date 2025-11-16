import os
from datetime import timedelta

# مفاتيح LINE
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET", "")

# مفتاح الإدارة
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "admin_whale_2025")

# مفاتيح Gemini AI (اختياري)
GEMINI_KEYS = [
    os.getenv("GEMINI_API_KEY_1"),
    os.getenv("GEMINI_API_KEY_2"),
    os.getenv("GEMINI_API_KEY_3")
]

# إعدادات النظام
CLEANUP_DAYS = 45
MAX_MESSAGES_PER_MINUTE = 10

# ألوان iOS
COLORS = {
    'primary': '#007AFF',
    'secondary': '#5856D6',
    'success': '#34C759',
    'bg_light': '#F8F9FA',
    'text_primary': '#1C1C1E',
    'text_secondary': '#8E8E93',
    'border': '#E5E5EA'
}
