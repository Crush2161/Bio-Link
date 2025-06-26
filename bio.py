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
    is_whitelisted, add_whitelist, remove_whitelist, get_whitelist,
    track_group, get_all_groups  # Add new group tracking functions
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

# Main bio checking function - this now tracks groups automatically
@app.on_message(filters.group & ~filters.service & ~filters.channel & ~filters.via_bot)
async def check_bio(client: Client, message):
    try:
        chat_id = message.chat.id
        
        # Track this group when any message is sent - THIS IS THE KEY PART!
        try:
            chat = await client.get_chat(chat_id)
            await track_group(chat_id, chat.title)
        except Exception as e:
            print(f"Error tracking group in check_bio: {e}")
        
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

# Bot Owner Commands - Enhanced with group tracking
@app.on_message(filters.command("listgroups") & filters.private)
async def list_tracked_groups(client: Client, message):
    """List all tracked groups - Owner only"""
    # Check if message has a user
    if not message.from_user:
        return
        
    user_id = message.from_user.id
    if not await is_bot_owner(user_id):
        return await message.reply_text("❌ **Access Denied!** This command is only for the bot owner.")
    
    try:
        groups = await get_all_groups()
        
        if not groups:
            return await message.reply_text(
                "📋 **No groups tracked yet!**\n\n"
                "Groups will be automatically tracked when:\n"
                "• Bot receives messages in groups\n"
                "• Commands like `/config`, `/free`, etc. are used\n"
                "• Bio checking is triggered\n\n"
                "Add the bot to groups and start using it!\n\n"
                "🔗 **Group tracking is now enabled** - MongoDB URI will save group IDs automatically!"
            )
        
        text = f"📋 **Tracked Groups ({len(groups)}):**\n\n"
        
        for i, chat_id in enumerate(groups[:20], 1):  # Show first 20 groups
            try:
                chat = await client.get_chat(chat_id)
                text += f"{i}. {chat.title}\n   ID: `{chat_id}`\n\n"
            except Exception as e:
                text += f"{i}. [Unknown Group]\n   ID: `{chat_id}`\n   Error: {str(e)[:50]}...\n\n"
        
        if len(groups) > 20:
            text += f"... and {len(groups) - 20} more groups"
        
        text += "\n✅ **Group tracking is working!** All groups are being saved to MongoDB automatically."
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📊 Stats", callback_data="owner_stats")],
            [InlineKeyboardButton("🗑️ Close", callback_data="close")]
        ])
        
        await message.reply_text(text, reply_markup=keyboard)
        
    except Exception as e:
        await message.reply_text(f"❌ **Error getting groups:** `{str(e)}`")

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
    print("🔗 Group tracking is now enabled - groups will be automatically saved to MongoDB!")
    print("📝 Use /listgroups command (owner only) to see tracked groups")
    app.run()
