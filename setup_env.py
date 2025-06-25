import os
import json
import sys

def save_config(config_data):
    with open("env_config.json", "w") as f:
        json.dump(config_data, f)
    print("Configuration saved successfully!")

def load_config():
    try:
        with open("env_config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "API_ID": "",
            "API_HASH": "",
            "BOT_TOKEN": "",
            "MONGO_URI": ""
        }

def setup_environment():
    config = load_config()
    
    print("BioLink Bot Setup")
    print("=================")
    print("Please provide the following information to set up your bot:\n")
    
    config["API_ID"] = input(f"Enter your Telegram API ID [{config['API_ID'] if config['API_ID'] else 'required'}]: ") or config["API_ID"]
    if not config["API_ID"]:
        print("API ID is required to run the bot.")
        return False
        
    config["API_HASH"] = input(f"Enter your Telegram API Hash [{config['API_HASH'][:5] + '...' if config['API_HASH'] else 'required'}]: ") or config["API_HASH"]
    if not config["API_HASH"]:
        print("API Hash is required to run the bot.")
        return False
        
    config["BOT_TOKEN"] = input(f"Enter your Bot Token [{config['BOT_TOKEN'][:5] + '...' if config['BOT_TOKEN'] else 'required'}]: ") or config["BOT_TOKEN"]
    if not config["BOT_TOKEN"]:
        print("Bot Token is required to run the bot.")
        return False
        
    config["MONGO_URI"] = input(f"Enter MongoDB Connection String [{config['MONGO_URI'][:10] + '...' if config['MONGO_URI'] else 'required'}]: ") or config["MONGO_URI"]
    if not config["MONGO_URI"]:
        print("MongoDB URI is required to run the bot.")
        return False
    
    save_config(config)
    
    # Set environment variables for the current session
    for key, value in config.items():
        os.environ[key] = value
    
    print("\nEnvironment variables set successfully!")
    return True

def run_bot():
    print("\nStarting BioLink Bot...")
    os.system("python bio.py")

if __name__ == "__main__":
    if setup_environment():
        user_input = input("\nDo you want to run the bot now? (y/n): ")
        if user_input.lower() == 'y':
            run_bot()
        else:
            print("\nYou can run the bot later using the command: python bio.py")
    else:
        print("\nSetup incomplete. Please run the setup again and provide all required information.")
