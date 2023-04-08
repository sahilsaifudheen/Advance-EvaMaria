import logging
from typing import Optional

from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database.connections_mdb import add_connection, all_connections, if_active, delete_connection
from info import ADMINS


logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)


@Client.on_message((filters.private | filters.group) & filters.command('connect'))
async def add_connection_handler(client: Client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"You are an anonymous admin. Use /connect {message.chat.id} in PM")

    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        try:
            _, group_id = message.text.split(" ", 1)
        except ValueError:
            await message.reply_text(
                "<b>Enter in correct format!</b>\n\n"
                "<code>/connect groupid</code>\n\n"
                "<i>Get your Group id by adding this bot to your group and use  <code>/id</code></i>",
                quote=True
            )
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        group_id = message.chat.id

    try:
        chat_member = await client.get_chat_member(group_id, userid)
        if (
            chat_member.status not in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER)
            and userid not in ADMINS
        ):
            await message.reply_text("You should be an admin in given group!", quote=True)
            return
    except Exception as e:
        logger.exception(e)
        await message.reply_text(
            "Invalid Group ID!\n\nIf correct, make sure I'm present in your group!!",
            quote=True,
        )
        return

    try:
        chat_member = await client.get_chat_member(group_id, "me")
        if chat_member.status != enums.ChatMemberStatus.ADMINISTRATOR:
            await message.reply_text("Add me as an admin in group", quote=True)
            return

        chat = await client.get_chat(group_id)
        title = chat.title

        addcon = await add_connection(str(group_id), str(userid))
        if addcon:
            await message.reply_text(
                f"Successfully connected to **{title}**\nNow manage your group from my pm!",
                quote=True,
                parse_mode=enums.ParseMode.MARKDOWN
            )

            if chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
                await client.send_message(
                    userid,
                    f"Connected to **{title}**
