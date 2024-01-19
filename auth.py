from telethon.sync import TelegramClient

from config import api_id, api_hash, phone_number, session_name

client = TelegramClient(session_name, api_id, api_hash)
client.start(phone_number)
client.disconnect()