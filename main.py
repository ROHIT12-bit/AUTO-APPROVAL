# 𝐌𝐀𝐃𝐄 𝐁𝐘 𝐑𝐎𝐇𝐈𝐓 | 𝐁𝐎𝐓𝐒𝐊𝐈𝐍𝐆𝐃𝐎𝐌𝐒
# 𝐓𝐆 𝐈𝐃 : @𝐁𝐎𝐓𝐒𝐊𝐈𝐍𝐆𝐃𝐎𝐌𝐒
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐒 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄

import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ChatJoinRequest
import config
import html

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

if not config.BOT_TOKEN or not config.API_ID or not config.API_HASH:
    raise RuntimeError("Set BOT_TOKEN, API_ID and API_HASH in config.py")

app = Client("auto_approve_bot",
             bot_token=config.BOT_TOKEN,
             api_id=config.API_ID,
             api_hash=config.API_HASH)

WELCOME_CAPTION = (
    f'🎀 <b>Hey sweetie ROHIT⭐✨</b>\n\n'
    f'<b>ACCESS HAS BEEN GRANTED — WELCOME TO Auto ongoing stardust !</b>\n\n'
    f'<i>{html.escape(config.FOOTER)}</i>'
)

START_CAPTION = (
    f'🎀 <b>Hey sweetie ROHIT⭐✨</b>\n\n'
    f'<b>ACCESS HAS BEEN GRANTED — WELCOME TO Auto ongoing stardust !</b>\n\n'
    f'<i>{html.escape(config.FOOTER)}</i>\n\n'
    f'<small>Bot made by {config.OWNER_USERNAME}</small>'
)

START_KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton("Main Channel", url=config.MAIN_CHANNEL)],
    [InlineKeyboardButton("Support", url=config.SUPPORT_LINK),
     InlineKeyboardButton("Click here", url=config.MAIN_CHANNEL)]
])

@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    try:
        await client.send_photo(
            chat_id=message.chat.id,
            photo=config.WELCOME_IMAGE,
            caption=START_CAPTION,
            reply_markup=START_KEYBOARD,
            parse_mode="html"
        )
    except Exception as e:
        logging.exception("Failed to send start message: %s", e)
        await message.reply_text("Bot is active. Contact the owner if you need help.")

@app.on_chat_join_request()
async def on_join_request(client: Client, join_request: ChatJoinRequest):
    chat = join_request.chat
    user = join_request.from_user
    chat_id = chat.id
    user_id = user.id

    try:
        if config.AUTO_APPROVE_INSTANT:
            await client.approve_chat_join_request(chat_id, user_id)
            logging.info("Approved %s (%s) to %s", user.first_name, user_id, chat.title)

            if config.SEND_WELCOME_IN_CHAT:
                text = (
                    f'🎉 <b>Hey {html.escape(user.first_name)}!</b>\n\n'
                    f'Access has been <b>GRANTED</b> — welcome to <b>{html.escape(chat.title)}</b>!\n\n'
                    f'<i>{html.escape(config.FOOTER)}</i>'
                )
                try:
                    await client.send_photo(
                        chat_id=chat_id,
                        photo=config.WELCOME_IMAGE,
                        caption=text,
                        parse_mode="html"
                    )
                except Exception:
                    await client.send_message(chat_id, text, parse_mode="html")

            if config.LOG_CHAT_ID:
                await client.send_message(
                    config.LOG_CHAT_ID,
                    f"✅ Approved <a href='tg://user?id={user_id}'>{html.escape(user.first_name)}</a> ({user_id}) to {chat.title}.",
                    parse_mode="html"
                )
        else:
            await client.decline_chat_join_request(chat_id, user_id)
            if config.LOG_CHAT_ID:
                await client.send_message(
                    config.LOG_CHAT_ID,
                    f"❌ Declined join request from <a href='tg://user?id={user_id}'>{html.escape(user.first_name)}</a> ({user_id}) in {chat.title}.",
                    parse_mode="html"
                )

    except Exception as e:
        logging.exception("Error handling join request: %s", e)
        if config.LOG_CHAT_ID:
            try:
                await client.send_message(config.LOG_CHAT_ID, f"Error handling join request for {user_id}: {e}")
            except Exception:
                pass

if __name__ == "__main__":
    logging.info("Starting Auto Approval Bot...")
    app.run()
