"""
Author: Crush Forever 
User: https://t.me/Forever_Crush
Channel: https://t.me/Crush_Forever
"""

from pyrogram import Client, filters, errors, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions

from helper.utils import (
    is_admin, is_bot_owner,
    get_config, update_config,
    increment_warning, reset_warnings,
    is_whitelisted, add_whitelist, remove_whitelist, get_whitelist
)

from config import (
    API_ID,
    API_HASH,
    BOT_TOKEN,
    URL_PATTERN,
    BOT_OWNER
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

@app.on_message(filters.command("start") & ~filters.via_bot)
async def start_handler(client: Client, message):
    try:
        chat_id = message.chat.id
        
        # Check if message has a user
        if not message.from_user:
            return
            
        user_id = message.from_user.id
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
        
        # Create keyboard based on chat type and user
        buttons = [[InlineKeyboardButton("➕ 𝐀𝐝𝐝 𝐌𝐞 𝐭𝐨 𝐘𝐨𝐮𝐫 𝐆𝐫𝐨𝐮𝐩", url=add_url)]]
        
        # Add owner button if it's private chat and user is bot owner
        if chat_id > 0 and await is_bot_owner(user_id):
            buttons.append([InlineKeyboardButton("👑 𝐎𝐰𝐧𝐞𝐫 𝐏𝐚𝐧𝐞𝐥", callback_data="owner_panel")])
        
        buttons.append([
            InlineKeyboardButton("🛠️ 𝐒𝐮𝐩𝐩𝐨𝐫𝐭", url="https://t.me/Crush_Forever"),
            InlineKeyboardButton("🗑️ 𝐂𝐥𝐨𝐬𝐞", callback_data="close")
        ])
        
        kb = InlineKeyboardMarkup(buttons)
        await client.send_message(chat_id, text, reply_markup=kb)
        
    except Exception as e:
        print(f"Error in start handler: {e}")
        try:
            await message.reply_text("❌ An error occurred while processing your request.")
        except:
            pass
    
@app.on_message(filters.command("help") & ~filters.via_bot)
async def help_handler(client: Client, message):
    try:
        chat_id = message.chat.id
        
        # Check if message has a user (some messages might not have from_user)
        if not message.from_user:
            return
            
        user_id = message.from_user.id if message.from_user else None
        
        # If no user (channel message), return early
        if not user_id:
            return
        
        help_text = (
            "**🛠️ 𝐁𝐨𝐭 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬 & 𝐔𝐬𝐚𝐠𝐞**\n\n"
            "`/config` – ꜱᴇᴛ ᴡᴀʀɴ-ʟɪᴍɪᴛ & ᴘᴜɴɪꜱʜᴍᴇɴᴛ ᴍᴏᴅᴇ\n"
            "`/free` – ᴡʜɪᴛᴇʟɪꜱᴛ ᴀ ᴜꜱᴇʀ (ʀᴇᴘʟʏ ᴏʀ ᴜꜱᴇʀ/ɪᴅ)\n"
            "`/unfree` – ʀᴇᴍᴏᴠᴇ ꜰʀᴏᴍ ᴡʜɪᴛᴇʟɪꜱᴛ\n"
            "`/freelist` – ʟɪꜱᴛ ᴀʟʟ ᴡʜɪᴛᴇʟɪꜱᴛᴇᴅ ᴜꜱᴇʀꜱ\n"
            "`/adminlist` – ʟɪꜱᴛ ᴀʟʟ ɢʀᴏᴜᴘ ᴀᴅᴍɪɴꜱ\n\n"
            "**𝐖𝐡𝐞𝐧 𝐬𝐨𝐦𝐞𝐨𝐧𝐞 𝐰𝐢𝐭𝐡 𝐚 𝐔𝐑𝐋 𝐢𝐧 𝐭𝐡𝐞𝐢𝐫 𝐛𝐢𝐨 𝐩𝐨𝐬𝐭𝐬, 𝐈'𝐥𝐥:**\n"
            " 1. ⚠️ ᴡᴀʀɴ ᴛʜᴇᴍ\n"
            " 2. 🔇 ᴍᴜᴛᴇ ɪꜢ ᴛʜᴇʏ ᴇxᴄᴇᴇᴅ ʟɪᴍɪᴛ\n"
            " 3. 🔨 ʙᴀɴ ɪꜢ ꜱᴇᴛ ᴛᴏ ʙᴀɴ\n\n"
            "**𝐔𝐬𝐞 𝐭𝐡𝐞 𝐢𝐧𝐥𝐢𝐧𝐞 𝐛𝐮𝐭𝐭𝐨𝐧𝐬 𝐨𝐧 𝐰𝐚𝐫𝐧𝐢𝐧𝐠𝐬 𝐭𝐨 𝐜𝐚𝐧𝐜𝐞𝐥 𝐨𝐫 𝐰𝐡𝐢𝐭𝐞𝐥𝐢𝐬𝐭**"
        )
        
        # Add bot owner commands if user is the bot owner
        if await is_bot_owner(user_id):
            help_text += (
                "\n\n👑 **𝐁𝐨𝐭 𝐎𝐰𝐧𝐞𝐫 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬:**\n"
                "`/stats` – ᴠɪᴇᴡ ʙᴏᴛ ꜱᴛᴀᴛɪꜱᴛɪᴄꜱ (ᴘʀɪᴠᴀᴛᴇ)\n"
                "`/broadcast` – ꜱᴇɴᴅ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ᴀʟʟ ɢʀᴏᴜᴘꜱ (ᴘʀɪᴠᴀᴛᴇ)\n"
                "`/globalban` – ɢʟᴏʙᴀʟ ʙᴀɴ ᴜꜱᴇʀ (ᴘʀɪᴠᴀᴛᴇ)\n\n"
                "✨ **You have owner privileges in all groups!**"
            )
        
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🗑️ 𝐂𝐥𝐨𝐬𝐞", callback_data="close")]
        ])
        await client.send_message(chat_id, help_text, reply_markup=kb)
    except Exception as e:
        print(f"Error in help_handler: {e}")

@app.on_message(filters.group & filters.command("config") & ~filters.via_bot)
async def configure(client: Client, message):
    try:
        chat_id = message.chat.id
        
        # Check if message has a user
        if not message.from_user:
            return
            
        user_id = message.from_user.id
        if not (await is_admin(client, chat_id, user_id) or await is_bot_owner(user_id)):
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
        
    except Exception as e:
        print(f"Error in configure handler: {e}")
        try:
            await message.reply_text("❌ An error occurred while processing your request.")
        except:
            pass

@app.on_message(filters.group & filters.command("free") & ~filters.via_bot)
async def command_free(client: Client, message):
    try:
        chat_id = message.chat.id
        
        # Check if message has a user
        if not message.from_user:
            return
            
        user_id = message.from_user.id
        if not (await is_admin(client, chat_id, user_id) or await is_bot_owner(user_id)):
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
        
    except Exception as e:
        print(f"Error in free command handler: {e}")
        try:
            await message.reply_text("❌ An error occurred while processing your request.")
        except:
            pass

@app.on_message(filters.group & filters.command("unfree") & ~filters.via_bot)
async def command_unfree(client: Client, message):
    try:
        chat_id = message.chat.id
        
        # Check if message has a user
        if not message.from_user:
            return
            
        user_id = message.from_user.id
        if not (await is_admin(client, chat_id, user_id) or await is_bot_owner(user_id)):
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
        
    except Exception as e:
        print(f"Error in unfree command handler: {e}")
        try:
            await message.reply_text("❌ An error occurred while processing your request.")
        except:
            pass

@app.on_message(filters.group & filters.command("freelist"))
async def command_freelist(client: Client, message):
    try:
        chat_id = message.chat.id
        
        # Check if message has a user
        if not message.from_user:
            return
            
        user_id = message.from_user.id
        if not (await is_admin(client, chat_id, user_id) or await is_bot_owner(user_id)):
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
        
    except Exception as e:
        print(f"Error in freelist command handler: {e}")
        try:
            await message.reply_text("❌ An error occurred while processing your request.")
        except:
            pass

@app.on_callback_query()
async def callback_handler(client: Client, callback_query):
    try:
        data = callback_query.data
        chat_id = callback_query.message.chat.id
        
        # Check if callback has a user
        if not callback_query.from_user:
            return await callback_query.answer("❌ Invalid user!", show_alert=True)
            
        user_id = callback_query.from_user.id
        
        # Check if user is admin or bot owner for regular callbacks
        try:
            # Handle close button first (special case)
            if data == "close":
                # In private chats, allow everyone to close their own messages
                if chat_id > 0:  # Private chat
                    return await callback_query.message.delete()
                # In groups, check admin permissions
                else:
                    if await is_admin(client, chat_id, user_id) or await is_bot_owner(user_id):
                        return await callback_query.message.delete()
                    else:
                        return await callback_query.answer("❌ Only admins can close messages", show_alert=True)
            
            # For other actions, check admin permissions
            if chat_id > 0:  # Private chat
                # For other actions in private chat, only allow bot owner
                is_user_admin = await is_bot_owner(user_id)
            else:  # Group chat
                is_user_admin = await is_admin(client, chat_id, user_id) or await is_bot_owner(user_id)
        except Exception as e:
            print(f"Error checking admin status in callback: {e}")
            # Allow bot owner even if admin check fails
            if await is_bot_owner(user_id):
                is_user_admin = True
            else:
                return await callback_query.answer("❌ Error checking permissions", show_alert=True)
            
        # Handle owner panel callback
        if data == "owner_panel":
            if not await is_bot_owner(user_id):
                return await callback_query.answer("❌ Access denied!", show_alert=True)
            
            owner_text = f"""
👑 **Bot Owner Panel** 👑

🤖 **Owner:** `{BOT_OWNER}`
✅ **Status:** Active

**Available Commands:**
• `/stats` - View bot statistics
• `/broadcast` - ꜱᴇɴᴅ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ᴀʟʟ ɢʀᴏᴜᴘꜱ  
• `/globalban` - ɢʟᴏʙᴀʟ ʙᴀɴ ᴜꜱᴇʀ
• `/adminlist` - Enhanced admin list

**Owner Privileges:**
✨ Exempt from bio checking in all groups
✨ Admin access in all groups
✨ Global management capabilities

Use the buttons below for quick actions:
            """
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("📊 View Stats", callback_data="owner_stats")],
                [InlineKeyboardButton("📡 Quick Broadcast", callback_data="quick_broadcast")],
                [InlineKeyboardButton("🔄 Refresh Panel", callback_data="owner_panel")],
                [InlineKeyboardButton("🗑️ Close", callback_data="close")]
            ])
            
            try:
                await safe_edit_message(callback_query.message, owner_text, keyboard)
            except errors.MessageNotModified:
                pass  # Message content is the same, ignore
            return await callback_query.answer("👑 Owner Panel Loaded!")
        
        # Handle owner stats callback
        if data == "owner_stats":
            if not await is_bot_owner(user_id):
                return await callback_query.answer("❌ Access denied!", show_alert=True)
            
            try:
                from helper.utils import db
                
                # Get statistics from database
                total_groups = await db.punishments.count_documents({})
                total_warnings = await db.warnings.count_documents({})
                total_whitelisted = await db.whitelists.count_documents({})
                
                # Get bot info
                bot = await client.get_me()
                
                stats_text = f"""
🤖 **Bot Statistics** 📊

**Bot Info:**
• Name: {bot.first_name}
• Username: @{bot.username}
• ID: `{bot.id}`

**Database Stats:**
• Total Groups: `{total_groups}`
• Total Warnings: `{total_warnings}`  
• Total Whitelisted Users: `{total_whitelisted}`

**Owner:** `{BOT_OWNER}`
🔄 **Last Updated:** Just now
                """
                
                keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔄 Refresh Stats", callback_data="owner_stats")],
                    [InlineKeyboardButton("👑 Back to Panel", callback_data="owner_panel")],
                    [InlineKeyboardButton("🗑️ Close", callback_data="close")]
                ])
                
                try:
                    await safe_edit_message(callback_query.message, stats_text, keyboard)
                except errors.MessageNotModified:
                    pass  # Message content is the same, ignore
                return await callback_query.answer("📊 Stats Updated!")
                
            except Exception as e:
                return await callback_query.answer(f"❌ Error: {str(e)}", show_alert=True)
        
        # Handle quick broadcast callback
        if data == "quick_broadcast":
            if not await is_bot_owner(user_id):
                return await callback_query.answer("❌ Access denied!", show_alert=True)
            
            broadcast_text = """
📡 **Quick Broadcast**

To send a message to all groups:
1. Use `/broadcast <your message>`
2. Or reply to any message with `/broadcast`

**Example:**
`/broadcast 🚨 Important announcement for all groups!`

**Note:** This feature works only in private chat with the bot.
            """
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("👑 Back to Panel", callback_data="owner_panel")],
                [InlineKeyboardButton("🗑️ Close", callback_data="close")]
            ])
            
            try:
                await callback_query.message.edit_text(broadcast_text, reply_markup=keyboard)
            except errors.MessageNotModified:
                pass  # Message content is the same, ignore
            return await callback_query.answer("📡 Broadcast Info Displayed!")
        
        # For group commands, check admin permissions
        if chat_id < 0 and not is_user_admin:  # Group chat and not admin
            return await callback_query.answer("❌ You are not administrator", show_alert=True)

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
            await safe_edit_message(callback_query.message, "**Choose penalty for users with links in bio:**", kb)
            return await callback_query.answer()

        if data == "warn":
            _, selected_limit, _ = await get_config(chat_id)
            kb = InlineKeyboardMarkup([
                [InlineKeyboardButton(f"3 ✅" if selected_limit==3 else "3", callback_data="warn_3"),
                 InlineKeyboardButton(f"4 ✅" if selected_limit==4 else "4", callback_data="warn_4"),
                 InlineKeyboardButton(f"5 ✅" if selected_limit==5 else "5", callback_data="warn_5")],
                [InlineKeyboardButton("Back", callback_data="back"), InlineKeyboardButton("Close", callback_data="close")]
            ])
            return await safe_edit_message(callback_query.message, "**Select number of warns before penalty:**", kb)

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
            await safe_edit_message(callback_query.message, "**Punishment selected:**", kb)
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

@app.on_message(filters.group & ~filters.service & ~filters.channel & ~filters.via_bot)
async def check_bio(client: Client, message):
    try:
        chat_id = message.chat.id
        
        # Check if message has a user (not from channel or automated)
        if not message.from_user:
            return
            
        user_id = message.from_user.id
        
        # Check if user is admin, whitelisted, or bot owner - bot owner is always exempt
        if (await is_admin(client, chat_id, user_id) or 
            await is_whitelisted(chat_id, user_id) or 
            await is_bot_owner(user_id)):
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
    except Exception as e:
        print(f"Error in check_bio: {e}")
        # Don't send error messages to users, just log them

# Bot Owner Commands - These commands work only for the bot owner
@app.on_message(filters.command("stats") & filters.private)
async def bot_stats(client: Client, message):
    """Bot statistics command - Owner only"""
    # Check if message has a user
    if not message.from_user:
        return
        
    user_id = message.from_user.id
    if not await is_bot_owner(user_id):
        return await message.reply_text("❌ **Access Denied!** This command is only for the bot owner.")
    
    try:
        from helper.utils import db
        
        # Get statistics from database
        total_groups = await db.punishments.count_documents({})
        total_warnings = await db.warnings.count_documents({})
        total_whitelisted = await db.whitelists.count_documents({})
        
        # Get bot info
        bot = await client.get_me()
        
        stats_text = f"""
🤖 **Bot Statistics** 📊

**Bot Info:**
• Name: {bot.first_name}
• Username: @{bot.username}
• ID: `{bot.id}`

**Database Stats:**
• Total Groups: `{total_groups}`
• Total Warnings: `{total_warnings}`  
• Total Whitelisted Users: `{total_whitelisted}`

**Owner:** `{BOT_OWNER if BOT_OWNER else 'Not Set'}`
        """
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Refresh", callback_data="owner_stats")],
            [InlineKeyboardButton("👑 Owner Panel", callback_data="owner_panel")],
            [InlineKeyboardButton("🗑️ Close", callback_data="close")]
        ])
        
        await message.reply_text(stats_text, reply_markup=keyboard)
        
    except Exception as e:
        await message.reply_text(f"❌ **Error getting stats:** `{str(e)}`")

@app.on_message(filters.command("broadcast") & filters.private)
async def broadcast_message(client: Client, message):
    """Broadcast message to all groups - Owner only"""
    # Check if message has a user
    if not message.from_user:
        return
        
    user_id = message.from_user.id
    if not await is_bot_owner(user_id):
        return await message.reply_text("❌ **Access Denied!** This command is only for the bot owner.")
    
    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text(
            "❗ **Usage:** `/broadcast <message>` or reply to a message with `/broadcast`\n\n"
            "This will send the message to all groups where the bot is active."
        )
    
    # Get broadcast message
    broadcast_msg = None
    broadcast_text = None
    
    if message.reply_to_message:
        broadcast_msg = message.reply_to_message
    else:
        broadcast_text = " ".join(message.command[1:])
        
    try:
        from helper.utils import db
        
        # Get all group IDs
        groups = await db.punishments.distinct("chat_id")
        
        if not groups:
            return await message.reply_text("❌ **No groups found in database!**")
        
        sent_count = 0
        failed_count = 0
        
        status_msg = await message.reply_text(f"📡 **Broadcasting to {len(groups)} groups...**")
        
        for chat_id in groups:
            try:
                if broadcast_msg:
                    await broadcast_msg.copy(chat_id)
                elif broadcast_text:
                    await client.send_message(chat_id, broadcast_text)
                sent_count += 1
            except Exception as e:
                failed_count += 1
                print(f"Failed to broadcast to {chat_id}: {e}")
        
        result_text = f"""
✅ **Broadcast Complete!**

📊 **Results:**
• Sent: `{sent_count}` groups
• Failed: `{failed_count}` groups
• Total: `{len(groups)}` groups
        """
        
        await status_msg.edit_text(result_text)
        
    except Exception as e:
        await message.reply_text(f"❌ **Error during broadcast:** `{str(e)}`")

@app.on_message(filters.command("adminlist"))
async def admin_list(client: Client, message):
    """List all admins in current group - Enhanced for owner"""
    chat_id = message.chat.id
    
    # Check if message has a user
    if not message.from_user:
        return
        
    user_id = message.from_user.id
    
    # Check if user is admin or bot owner
    if not (await is_admin(client, chat_id, user_id) or await is_bot_owner(user_id)):
        return await message.reply_text("❌ **You need to be an admin to use this command!**")
    
    try:
        # Use a simpler approach - get chat administrators
        chat = await client.get_chat(chat_id)
        admin_text = f"👨‍💼 **Group Administrators for {chat.title}:**\n\n"
        
        # Add basic info for now - we'll try to get more details later
        admin_text += "ℹ️ **Note:** Admin list feature is being updated.\n"
        admin_text += "Use this command again in groups for full admin list.\n\n"
        
        # Add owner info if bot owner is checking
        if await is_bot_owner(user_id):
            admin_text += f"🤖 **Bot Owner:** `{BOT_OWNER}`\n"
            admin_text += "✅ **You have bot owner privileges in all groups!**"
            
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🗑️ Close", callback_data="close")]])
        await message.reply_text(admin_text, reply_markup=keyboard)
        
    except Exception as e:
        await message.reply_text(f"❌ **Error getting admin list:** `{str(e)}`")

@app.on_message(filters.command("globalban") & filters.private)
async def global_ban_user(client: Client, message):
    """Global ban a user from all groups - Owner only"""
    # Check if message has a user
    if not message.from_user:
        return
        
    user_id = message.from_user.id
    if not await is_bot_owner(user_id):
        return await message.reply_text("❌ **Access Denied!** This command is only for the bot owner.")
    
    if len(message.command) < 2:
        return await message.reply_text(
            "❗ **Usage:** `/globalban <user_id>`\n\n"
            "This will ban the user from all groups where the bot is admin."
        )
    
    try:
        target_user_id = int(message.command[1])
        
        # Don't allow banning the owner or other bots
        if target_user_id == BOT_OWNER:
            return await message.reply_text("❌ **Cannot ban the bot owner!**")
            
        from helper.utils import db
        
        # Get all group IDs
        groups = await db.punishments.distinct("chat_id")
        
        if not groups:
            return await message.reply_text("❌ **No groups found in database!**")
        
        banned_count = 0
        failed_count = 0
        
        status_msg = await message.reply_text(f"⚡ **Global banning user {target_user_id} from {len(groups)} groups...**")
        
        for chat_id in groups:
            try:
                await client.ban_chat_member(chat_id, target_user_id)
                banned_count += 1
            except Exception as e:
                failed_count += 1
                print(f"Failed to ban {target_user_id} from {chat_id}: {e}")
        
        result_text = f"""
⚡ **Global Ban Complete!**

🎯 **Target:** `{target_user_id}`

📊 **Results:**
• Banned from: `{banned_count}` groups
• Failed: `{failed_count}` groups
• Total: `{len(groups)}` groups
        """
        
        await status_msg.edit_text(result_text)
        
    except ValueError:
        await message.reply_text("❌ **Invalid user ID! Please provide a valid numeric user ID.**")
    except Exception as e:
        await message.reply_text(f"❌ **Error during global ban:** `{str(e)}`")

async def safe_edit_message(message, text, keyboard=None):
    """Safely edit a message, ignoring 'not modified' errors"""
    try:
        if keyboard:
            await message.edit_text(text, reply_markup=keyboard)
        else:
            await message.edit_text(text)
    except errors.MessageNotModified:
        pass  # Message content is the same, ignore
    except Exception as e:
        print(f"Error editing message: {e}")

if __name__ == "__main__":
    # Print startup information
    print("🤖 BioLink Protector Bot Starting...")
    print(f"📊 Bot Owner: {'Configured' if BOT_OWNER else 'Not Set'}")
    if BOT_OWNER:
        print(f"👑 Owner ID: {BOT_OWNER}")
        print("✅ Bot owner will have access to all groups and special commands!")
    else:
        print("⚠️  Bot owner not configured. Set BOT_OWNER in environment or config file.")
    print("🚀 Starting bot...")
    app.run()
