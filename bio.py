"""
Author: Crush Forever 
User: https://t.me/Forever_Crush
Channel: https://t.me/Crush_Forever
"""

from pyrogram import Client, filters, errors
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions

from helper.utils import (
    is_admin,
    get_config, update_config,
    increment_warning, reset_warnings,
    is_whitelisted, add_whitelist, remove_whitelist, get_whitelist
)

from config import (
    API_ID,
    API_HASH,
    BOT_TOKEN,
    URL_PATTERN
)

app = Client(
    "biolink_protector_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

async def get_user_info_safe(client: Client, user_id: int):
    """Safely get user information with fallback"""
    try:
        users = await client.get_users(user_id)
        # get_users returns a list even for single user
        user = users[0] if isinstance(users, list) else users
        full_name = f"{user.first_name}{(' ' + user.last_name) if user.last_name else ''}"
        mention = f"[{full_name}](tg://user?id={user_id})"
        bio = getattr(user, 'bio', '') or ""
        return full_name, mention, bio
    except Exception as e:
        print(f"Error getting user info for {user_id}: {e}")
        fallback_name = f"User {user_id}"
        fallback_mention = f"[{fallback_name}](tg://user?id={user_id})"
        return fallback_name, fallback_mention, ""

@app.on_message(filters.command("start"))
async def start_handler(client: Client, message):
    chat_id = message.chat.id
    bot = await client.get_me()
    add_url = f"https://t.me/{bot.username}?startgroup=true"
    text = (
        "**✨ 𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 𝐁𝐈𝐎𝐋𝐈𝐍𝐊 𝐏𝐑𝐎𝐓𝐄𝐂𝐓𝐎𝐑 𝐁𝐎𝐓! ✨**\n\n"
        "**🔹 𝐊𝐞𝐲 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬:**\n"
        "   • 𝐀𝐮𝐭𝐨𝐦𝐚𝐭𝐢𝐜 𝐔𝐑𝐋 𝐝𝐞𝐭𝐞𝐜𝐭𝐢𝐨𝐧 𝐢𝐧 𝐮𝐬𝐞𝐫 𝐛𝐢𝐨𝐬\n"
        "   • 𝐂𝐮𝐬𝐭𝐨𝐦𝐢𝐳𝐚𝐛𝐥𝐞 𝐰𝐚𝐫𝐧𝐢𝐧𝐠 𝐥𝐢𝐦𝐢𝐭\n"
        "   • 𝐀𝐮𝐭𝐨-𝐦𝐮𝐭𝐞 𝐨𝐫 𝐛𝐚𝐧 𝐰𝐡𝐞𝐧 𝐥𝐢𝐦𝐢𝐭 𝐢𝐬 𝐫𝐞𝐚𝐜𝐡𝐞𝐝\n"
        "   • 𝐖𝐡𝐢𝐭𝐞𝐥𝐢𝐬𝐭 𝐦𝐚𝐧𝐚𝐠𝐞𝐦𝐞𝐧𝐭 𝐟𝐨𝐫 𝐭𝐫𝐮𝐬𝐭𝐞𝐝 𝐮𝐬𝐞𝐫𝐬\n\n"
        "**𝐔𝐬𝐞 /help 𝐭𝐨 𝐬𝐞𝐞 𝐚𝐥𝐥 𝐚𝐯𝐚𝐢𝐥𝐚𝐛𝐥𝐞 𝐜𝐨𝐦𝐦𝐚𝐧𝐝𝐬.**"
    )
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ 𝐀𝐝𝐝 𝐌𝐞 𝐭𝐨 𝐘𝐨𝐮𝐫 𝐆𝐫𝐨𝐮𝐩", url=add_url)],
        [
            InlineKeyboardButton("🛠️ 𝐒𝐮𝐩𝐩𝐨𝐫𝐭", url="https://t.me/Crush_Forever"),
            InlineKeyboardButton("🗑️ 𝐂𝐥𝐨𝐬𝐞", callback_data="close")
        ]
    ])
    await client.send_message(chat_id, text, reply_markup=kb)
    
@app.on_message(filters.command("help"))
async def help_handler(client: Client, message):
    chat_id = message.chat.id
    help_text = (
        "**🛠️ 𝐁𝐨𝐭 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬 & 𝐔𝐬𝐚𝐠𝐞**\n\n"
        "`/config` – ꜱᴇᴛ ᴡᴀʀɴ-ʟɪᴍɪᴛ & ᴘᴜɴɪꜱʜᴍᴇɴᴛ ᴍᴏᴅᴇ\n"
        "`/free` – ᴡʜɪᴛᴇʟɪꜱᴛ ᴀ ᴜꜱᴇʀ (ʀᴇᴘʟʏ ᴏʀ ᴜꜱᴇʀ/ɪᴅ)\n"
        "`/unfree` – ʀᴇᴍᴏᴠᴇ ꜰʀᴏᴍ ᴡʜɪᴛᴇʟɪꜱᴛ\n"
        "`/freelist` – ʟɪꜱᴛ ᴀʟʟ ᴡʜɪᴛᴇʟɪꜱᴛᴇᴅ ᴜꜱᴇʀꜱ\n\n"
        "**𝐖𝐡𝐞𝐧 𝐬𝐨𝐦𝐞𝐨𝐧𝐞 𝐰𝐢𝐭𝐡 𝐚 𝐔𝐑𝐋 𝐢𝐧 𝐭𝐡𝐞𝐢𝐫 𝐛𝐢𝐨 𝐩𝐨𝐬𝐭𝐬, 𝐈'𝐥𝐥:**\n"
        " 1. ⚠️ ᴡᴀʀɴ ᴛʜᴇᴍ\n"
        " 2. 🔇 ᴍᴜᴛᴇ ɪꜰ ᴛʜᴇʏ ᴇxᴄᴇᴇᴅ ʟɪᴍɪᴛ\n"
        " 3. 🔨 ʙᴀɴ ɪꜢ ꜱᴇᴛ ᴛᴏ ʙᴀɴ\n\n"
        "**𝐔𝐬𝐞 𝐭𝐡𝐞 𝐢𝐧𝐥𝐢𝐧𝐞 𝐛𝐮𝐭𝐭𝐨𝐧𝐬 𝐨𝐧 𝐰𝐚𝐫𝐧𝐢𝐧𝐠𝐬 𝐭𝐨 𝐜𝐚𝐧𝐜𝐞𝐥 𝐨𝐫 𝐰𝐡𝐢𝐭𝐞𝐥𝐢𝐬𝐭**"
    )
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🗑️ 𝐂𝐥𝐨𝐬𝐞", callback_data="close")]
    ])
    await client.send_message(chat_id, help_text, reply_markup=kb)

@app.on_message(filters.group & filters.command("config"))
async def configure(client: Client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if not await is_admin(client, chat_id, user_id):
        return

    mode, limit, penalty = await get_config(chat_id)
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Warn", callback_data="warn")],
        [
            InlineKeyboardButton("Mute ✅" if penalty == "mute" else "Mute", callback_data="mute"),
            InlineKeyboardButton("Ban ✅" if penalty == "ban" else "Ban", callback_data="ban")
        ],
        [InlineKeyboardButton("Close", callback_data="close")]
    ])
    await client.send_message(
        chat_id,
        "**Choose penalty for users with links in bio:**",
        reply_markup=keyboard
    )
    await message.delete()

@app.on_message(filters.group & filters.command("free"))
async def command_free(client: Client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if not await is_admin(client, chat_id, user_id):
        return

    if message.reply_to_message:
        target = message.reply_to_message.from_user
    elif len(message.command) > 1:
        arg = message.command[1]
        users = await client.get_users(int(arg) if arg.isdigit() else arg)
        target = users[0] if isinstance(users, list) else users
    else:
        return await client.send_message(chat_id, "**Reply or use /free user or id to whitelist someone.**")

    await add_whitelist(chat_id, target.id)
    await reset_warnings(chat_id, target.id)

    text = f"**✅ {target.mention} has been added to the whitelist**"
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🚫 Unwhitelist", callback_data=f"unwhitelist_{target.id}"),
            InlineKeyboardButton("🗑️ Close", callback_data="close")
        ]
    ])
    await client.send_message(chat_id, text, reply_markup=keyboard)

@app.on_message(filters.group & filters.command("unfree"))
async def command_unfree(client: Client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if not await is_admin(client, chat_id, user_id):
        return

    if message.reply_to_message:
        target = message.reply_to_message.from_user
    elif len(message.command) > 1:
        arg = message.command[1]
        users = await client.get_users(int(arg) if arg.isdigit() else arg)
        target = users[0] if isinstance(users, list) else users
    else:
        return await client.send_message(chat_id, "**Reply or use /unfree user or id to unwhitelist someone.**")

    if await is_whitelisted(chat_id, target.id):
        await remove_whitelist(chat_id, target.id)
        text = f"**🚫 {target.mention} has been removed from the whitelist**"
    else:
        text = f"**ℹ️ {target.mention} is not whitelisted.**"

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Whitelist", callback_data=f"whitelist_{target.id}"),
            InlineKeyboardButton("🗑️ Close", callback_data="close")
        ]
    ])
    await client.send_message(chat_id, text, reply_markup=keyboard)

@app.on_message(filters.group & filters.command("freelist"))
async def command_freelist(client: Client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if not await is_admin(client, chat_id, user_id):
        return

    ids = await get_whitelist(chat_id)
    if not ids:
        await client.send_message(chat_id, "**⚠️ No users are whitelisted in this group.**")
        return

    text = "**📋 Whitelisted Users:**\n\n"
    for i, uid in enumerate(ids, start=1):
        try:
            users = await client.get_users(uid)
            user = users[0] if isinstance(users, list) else users
            name = f"{user.first_name}{(' ' + user.last_name) if user.last_name else ''}"
            text += f"{i}: {name} [`{uid}`]\n"
        except:
            text += f"{i}: [User not found] [`{uid}`]\n"

    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🗑️ Close", callback_data="close")]])
    await client.send_message(chat_id, text, reply_markup=keyboard)

@app.on_callback_query()
async def callback_handler(client: Client, callback_query):
    try:
        data = callback_query.data
        chat_id = callback_query.message.chat.id
        user_id = callback_query.from_user.id
        
        # Check if user is admin with error handling
        try:
            is_user_admin = await is_admin(client, chat_id, user_id)
        except Exception as e:
            print(f"Error checking admin status in callback: {e}")
            return await callback_query.answer("❌ Error checking permissions", show_alert=True)
            
        if not is_user_admin:
            return await callback_query.answer("❌ You are not administrator", show_alert=True)

        if data == "close":
            return await callback_query.message.delete()

        if data == "back":
            mode, limit, penalty = await get_config(chat_id)
            kb = InlineKeyboardMarkup([
                [InlineKeyboardButton("Warn", callback_data="warn")],
                [
                    InlineKeyboardButton("Mute ✅" if penalty=="mute" else "Mute", callback_data="mute"),
                    InlineKeyboardButton("Ban ✅" if penalty=="ban" else "Ban", callback_data="ban")
                ],
                [InlineKeyboardButton("Close", callback_data="close")]
            ])
            await callback_query.message.edit_text("**Choose penalty for users with links in bio:**", reply_markup=kb)
            return await callback_query.answer()

        if data == "warn":
            _, selected_limit, _ = await get_config(chat_id)
            kb = InlineKeyboardMarkup([
                [InlineKeyboardButton(f"3 ✅" if selected_limit==3 else "3", callback_data="warn_3"),
                 InlineKeyboardButton(f"4 ✅" if selected_limit==4 else "4", callback_data="warn_4"),
                 InlineKeyboardButton(f"5 ✅" if selected_limit==5 else "5", callback_data="warn_5")],
                [InlineKeyboardButton("Back", callback_data="back"), InlineKeyboardButton("Close", callback_data="close")]
            ])
            return await callback_query.message.edit_text("**Select number of warns before penalty:**", reply_markup=kb)

        if data in ["mute", "ban"]:
            await update_config(chat_id, penalty=data)
            mode, limit, penalty = await get_config(chat_id)
            kb = InlineKeyboardMarkup([
                [InlineKeyboardButton("Warn", callback_data="warn")],
                [
                    InlineKeyboardButton("Mute ✅" if penalty=="mute" else "Mute", callback_data="mute"),
                    InlineKeyboardButton("Ban ✅" if penalty=="ban" else "Ban", callback_data="ban")
                ],
                [InlineKeyboardButton("Close", callback_data="close")]
            ])
            await callback_query.message.edit_text("**Punishment selected:**", reply_markup=kb)
            return await callback_query.answer()

        if data.startswith("warn_"):
            count = int(data.split("_")[1])
            await update_config(chat_id, limit=count)
            kb = InlineKeyboardMarkup([
                [InlineKeyboardButton(f"3 ✅" if count==3 else "3", callback_data="warn_3"),
                 InlineKeyboardButton(f"4 ✅" if count==4 else "4", callback_data="warn_4"),
                 InlineKeyboardButton(f"5 ✅" if count==5 else "5", callback_data="warn_5")],
                [InlineKeyboardButton("Back", callback_data="back"), InlineKeyboardButton("Close", callback_data="close")]
            ])
            await callback_query.message.edit_text(f"**Warning limit set to {count}**", reply_markup=kb)
            return await callback_query.answer()

        if data.startswith(("unmute_", "unban_")):
            action, uid = data.split("_")
            target_id = int(uid)
            try:
                users = await client.get_users(target_id)
                user_obj = users[0] if isinstance(users, list) else users
                name = f"{user_obj.first_name}{(' ' + user_obj.last_name) if user_obj.last_name else ''}"
            except:
                name = f"User {target_id}"
            
            try:
                if action == "unmute":
                    await client.restrict_chat_member(chat_id, target_id, ChatPermissions(can_send_messages=True))
                else:
                    await client.unban_chat_member(chat_id, target_id)
                await reset_warnings(chat_id, target_id)
                msg = f"**{name} (`{target_id}`) has been {'unmuted' if action=='unmute' else 'unbanned'}**."

                kb = InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("Whitelist ✅", callback_data=f"whitelist_{target_id}"),
                        InlineKeyboardButton("🗑️ Close", callback_data="close")
                    ]
                ])
                await callback_query.message.edit_text(msg, reply_markup=kb)
            
            except errors.ChatAdminRequired:
                await callback_query.message.edit_text(f"I don't have permission to {action} users.")
            return await callback_query.answer()

        if data.startswith("cancel_warn_"):
            target_id = int(data.split("_")[-1])
            await reset_warnings(chat_id, target_id)
            try:
                users = await client.get_users(target_id)
                user_obj = users[0] if isinstance(users, list) else users
                full_name = f"{user_obj.first_name}{(' ' + user_obj.last_name) if user_obj.last_name else ''}"
                mention = f"[{full_name}](tg://user?id={target_id})"
            except:
                mention = f"User {target_id}"
            
            kb = InlineKeyboardMarkup([
                [InlineKeyboardButton("Whitelist✅", callback_data=f"whitelist_{target_id}"),
                 InlineKeyboardButton("🗑️ Close", callback_data="close")]
            ])
            await callback_query.message.edit_text(f"**✅ {mention} [`{target_id}`] has no more warnings!**", reply_markup=kb)
            return await callback_query.answer()

        if data.startswith("whitelist_"):
            target_id = int(data.split("_")[1])
            await add_whitelist(chat_id, target_id)
            await reset_warnings(chat_id, target_id)
            try:
                users = await client.get_users(target_id)
                user_obj = users[0] if isinstance(users, list) else users
                full_name = f"{user_obj.first_name}{(' ' + user_obj.last_name) if user_obj.last_name else ''}"
                mention = f"[{full_name}](tg://user?id={target_id})"
            except:
                mention = f"User {target_id}"
            
            kb = InlineKeyboardMarkup([
                [InlineKeyboardButton("🚫 Unwhitelist", callback_data=f"unwhitelist_{target_id}"),
                 InlineKeyboardButton("🗑️ Close", callback_data="close")]
            ])
            await callback_query.message.edit_text(f"**✅ {mention} [`{target_id}`] has been whitelisted!**", reply_markup=kb)
            return await callback_query.answer()

        if data.startswith("unwhitelist_"):
            target_id = int(data.split("_")[1])
            await remove_whitelist(chat_id, target_id)
            try:
                users = await client.get_users(target_id)
                user_obj = users[0] if isinstance(users, list) else users
                full_name = f"{user_obj.first_name}{(' ' + user_obj.last_name) if user_obj.last_name else ''}"
                mention = f"[{full_name}](tg://user?id={target_id})"
            except:
                mention = f"User {target_id}"
            
            kb = InlineKeyboardMarkup([
                [InlineKeyboardButton("Whitelist✅", callback_data=f"whitelist_{target_id}"),
                 InlineKeyboardButton("🗑️ Close", callback_data="close")]
            ])
            await callback_query.message.edit_text(f"**❌ {mention} [`{target_id}`] has been removed from whitelist.**", reply_markup=kb)
            return await callback_query.answer()
            
    except Exception as e:
        print(f"Error in callback handler: {e}")
        try:
            await callback_query.answer("❌ An error occurred while processing your request", show_alert=True)
        except:
            pass

@app.on_message(filters.group)
async def check_bio(client: Client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if await is_admin(client, chat_id, user_id) or await is_whitelisted(chat_id, user_id):
        return

    # Get user info safely using our helper function
    full_name, mention, bio = await get_user_info_safe(client, user_id)

    if URL_PATTERN.search(bio):
        try:
            await message.delete()
        except errors.MessageDeleteForbidden:
            return await message.reply_text("Please grant me delete permission.")

        mode, limit, penalty = await get_config(chat_id)
        if mode == "warn":
            count = await increment_warning(chat_id, user_id)
            warning_text = (
                "**🚨 Warning Issued** 🚨\n\n"
                f"👤 **User:** {mention} `[{user_id}]`\n"
                "❌ **Reason:** URL found in bio\n"
                f"⚠️ **Warning:** {count}/{limit}\n\n"
                "**Notice: Please remove any links from your bio.**"
            )
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("❌ Cancel Warning", callback_data=f"cancel_warn_{user_id}"),
                 InlineKeyboardButton("✅ Whitelist", callback_data=f"whitelist_{user_id}")],
                [InlineKeyboardButton("🗑️ Close", callback_data="close")]
            ])
            sent = await message.reply_text(warning_text, reply_markup=keyboard)
            if count >= limit:
                try:
                    if penalty == "mute":
                        await client.restrict_chat_member(chat_id, user_id, ChatPermissions())
                        kb = InlineKeyboardMarkup([[InlineKeyboardButton("Unmute ✅", callback_data=f"unmute_{user_id}")]])
                        await sent.edit_text(f"**{mention} has been 🔇 muted for [Link In Bio].**", reply_markup=kb)
                    else:
                        await client.ban_chat_member(chat_id, user_id)
                        kb = InlineKeyboardMarkup([[InlineKeyboardButton("Unban ✅", callback_data=f"unban_{user_id}")]])
                        await sent.edit_text(f"**{mention} has been 🔨 banned for [Link In Bio].**", reply_markup=kb)
                
                except errors.ChatAdminRequired:
                    await sent.edit_text(f"**I don't have permission to {penalty} users.**")
        else:
            try:
                if mode == "mute":
                    await client.restrict_chat_member(chat_id, user_id, ChatPermissions())
                    kb = InlineKeyboardMarkup([[InlineKeyboardButton("Unmute", callback_data=f"unmute_{user_id}")]])
                    await message.reply_text(f"{mention} has been 🔇 muted for [Link In Bio].", reply_markup=kb)
                else:
                    await client.ban_chat_member(chat_id, user_id)
                    kb = InlineKeyboardMarkup([[InlineKeyboardButton("Unban", callback_data=f"unban_{user_id}")]])
                    await message.reply_text(f"{mention} has been 🔨 banned for [Link In Bio].", reply_markup=kb)
            except errors.ChatAdminRequired:
                return await message.reply_text(f"I don't have permission to {mode} users.")
    else:
        await reset_warnings(chat_id, user_id)

if __name__ == "__main__":
    app.run()
