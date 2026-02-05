from telethon import TelegramClient, events
import os

api_id = 28677153
api_hash = "eзаe75c3e7a6540def2c7cfb7e3c6516”

client = TelegramClient("self", api_id, api_hash)

cache = {}

MEDIA_DIR = "deleted_media"
os.makedirs(MEDIA_DIR, exist_ok=True)

@client.on(events.NewMessage)
async def save_message(event):
    msg = event.message
    cache[msg.id] = msg

    # دانلود مدیا فوری
    if msg.media:
        file = await msg.download_media(file=MEDIA_DIR)
        cache[msg.id].downloaded_file = file

@client.on(events.MessageDeleted)
async def deleted(event):
    for msg_id in event.deleted_ids:
        msg = cache.get(msg_id)
        if not msg:
            continue

        sender = await msg.get_sender()
        chat = await msg.get_chat()

        sender_name = sender.first_name if sender else "Unknown"
        chat_name = getattr(chat, 'title', 'Private Chat')

        text = msg.text if msg.text else "⛔️ متن نداشت"

        notify = f"""
🚨 پیام حذف شد!

👤 فرستنده: {sender_name}
💬 چت: {chat_name}
📝 متن:
{text}
"""
        await client.send_message("me", notify)

        # ارسال مدیا اگه وجود داشت
        if hasattr(msg, "downloaded_file") and msg.downloaded_file:
            await client.send_file(
                "me",
                msg.downloaded_file,
                caption="📎 فایل حذف‌شده"
            )

client.start()
client.run_until_disconnected()
