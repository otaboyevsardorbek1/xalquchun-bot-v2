# bot/data.py
"""
Bot uchun kerakli konstantalar va ma'lumotlar
"""
import os

# Bot token
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# Admin ID lar
OWNER_ID = int(os.getenv("OWNER_ID", "6646928202"))
ADMIN_IDS = [6646928202, 6684122507]  # Admin ID lar ro'yxati
ALL_OWNER_IDS = [6646928202, 6684122507]  # Barcha admin va owner ID lar

# Webhook
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST", "")

# Log
LOG_FILE = os.getenv("LOG_FILE", "bot.log")
MAX_LOG_SIZE_MB = int(os.getenv("MAX_LOG_SIZE_MB", "20"))

# Referral tizimi
MAX_TREE_DEPTH = int(os.getenv("MAX_TREE_DEPTH", "15"))
MAX_REWARD_LEVEL = 5  # Maksimal mukofot darajasi
LEVEL_REWARDS = {
    1: 100.0,
    2: 50.0,
    3: 25.0,
    4: 10.0,
    5: 5.0
}