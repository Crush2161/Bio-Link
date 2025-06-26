from typing import Optional

from pyrogram import Client, enums, filters
from motor.motor_asyncio import AsyncIOMotorClient

from config import (
    MONGO_URI,
    DEFAULT_CONFIG,
    DEFAULT_PUNISHMENT,
    DEFAULT_WARNING_LIMIT,
    BOT_OWNER
)

# Initialize MongoDB connection with error handling
try:
    mongo_client = AsyncIOMotorClient(MONGO_URI)
    db = mongo_client['telegram_bot_db']
    warnings_collection = db['warnings']
    punishments_collection = db['punishments']
    whitelists_collection = db['whitelists']
    groups_collection = db['groups']  # New collection for tracking groups
    print("✅ MongoDB connection initialized successfully")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    # Create dummy objects to prevent import errors
    mongo_client = None
    db = None
    warnings_collection = None
    punishments_collection = None
    whitelists_collection = None
    groups_collection = None

async def is_admin(client: Client, chat_id: int, user_id: int) -> bool:
    try:
        # Check if user is bot owner - bot owner is always admin
        if BOT_OWNER and user_id == BOT_OWNER:
            return True
        
        # Check if it's a private chat (DM) - admin check doesn't apply to DMs
        if chat_id > 0:  # Positive chat_id means private chat
            return False
            
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]
    except Exception as e:
        # Handle cases where chat is invalid, user not found, or bot doesn't have access
        print(f"Error checking admin status: {e}")
        # If we can't check admin status, still allow bot owner
        if BOT_OWNER and user_id == BOT_OWNER:
            return True
        return False
        return False

async def is_bot_owner(user_id: int) -> bool:
    """Check if user is the bot owner"""
    return bool(BOT_OWNER and user_id == BOT_OWNER)

async def get_config(chat_id: int):
    try:
        if not punishments_collection:
            return DEFAULT_CONFIG
        doc = await punishments_collection.find_one({'chat_id': chat_id})
        if doc:
            return doc.get('mode', 'warn'), doc.get('limit', DEFAULT_WARNING_LIMIT), doc.get('penalty', DEFAULT_PUNISHMENT)
        return DEFAULT_CONFIG
    except Exception as e:
        print(f"Error getting config: {e}")
        return DEFAULT_CONFIG

async def update_config(chat_id: int, mode=None, limit=None, penalty=None):
    try:
        if not punishments_collection:
            print("Warning: MongoDB not connected, config update skipped")
            return
        update = {}
        if mode is not None:
            update['mode'] = mode
        if limit is not None:
            update['limit'] = limit
        if penalty is not None:
            update['penalty'] = penalty
        if update:
            await punishments_collection.update_one(
                {'chat_id': chat_id},
                {'$set': update},
                upsert=True
            )
    except Exception as e:
        print(f"Error updating config: {e}")

async def increment_warning(chat_id: int, user_id: int) -> int:
    try:
        if not warnings_collection:
            print("Warning: MongoDB not connected, warning increment skipped")
            return 1
        await warnings_collection.update_one(
            {'chat_id': chat_id, 'user_id': user_id},
            {'$inc': {'count': 1}},
            upsert=True
        )
        doc = await warnings_collection.find_one({'chat_id': chat_id, 'user_id': user_id})
        return doc['count'] if doc else 1
    except Exception as e:
        print(f"Error incrementing warning: {e}")
        return 1

async def reset_warnings(chat_id: int, user_id: int):
    try:
        if not warnings_collection:
            print("Warning: MongoDB not connected, warning reset skipped")
            return
        await warnings_collection.delete_one({'chat_id': chat_id, 'user_id': user_id})
    except Exception as e:
        print(f"Error resetting warnings: {e}")

async def is_whitelisted(chat_id: int, user_id: int) -> bool:
    try:
        if not whitelists_collection:
            return False
        doc = await whitelists_collection.find_one({'chat_id': chat_id, 'user_id': user_id})
        return bool(doc)
    except Exception as e:
        print(f"Error checking whitelist: {e}")
        return False

async def add_whitelist(chat_id: int, user_id: int):
    try:
        if not whitelists_collection:
            print("Warning: MongoDB not connected, whitelist add skipped")
            return
        await whitelists_collection.update_one(
            {'chat_id': chat_id, 'user_id': user_id},
            {'$set': {'user_id': user_id}},
            upsert=True
        )
    except Exception as e:
        print(f"Error adding to whitelist: {e}")

async def remove_whitelist(chat_id: int, user_id: int):
    try:
        if not whitelists_collection:
            print("Warning: MongoDB not connected, whitelist remove skipped")
            return
        await whitelists_collection.delete_one({'chat_id': chat_id, 'user_id': user_id})
    except Exception as e:
        print(f"Error removing from whitelist: {e}")

async def get_whitelist(chat_id: int) -> list:
    try:
        if not whitelists_collection:
            return []
        cursor = whitelists_collection.find({'chat_id': chat_id})
        docs = await cursor.to_list(length=None)
        return [doc['user_id'] for doc in docs]
    except Exception as e:
        print(f"Error getting whitelist: {e}")
        return []

async def track_group(chat_id: int, chat_title: Optional[str] = None):
    """Track a group in the database"""
    try:
        if not groups_collection:
            print("Warning: MongoDB not connected, group tracking skipped")
            return
        if chat_id < 0:  # Only track groups (negative IDs)
            await groups_collection.update_one(
                {'chat_id': chat_id},
                {
                    '$set': {
                        'chat_id': chat_id,
                        'chat_title': chat_title,
                        'last_activity': None  # You can add timestamp if needed
                    }
                },
                upsert=True
            )
    except Exception as e:
        print(f"Error tracking group {chat_id}: {e}")

async def get_all_groups() -> list:
    """Get all tracked group IDs"""
    try:
        if not groups_collection:
            print("Warning: MongoDB not connected, returning empty group list")
            return []
        cursor = groups_collection.find({})
        docs = await cursor.to_list(length=None)
        return [doc['chat_id'] for doc in docs if doc.get('chat_id')]
    except Exception as e:
        print(f"Error getting groups: {e}")
        return []
