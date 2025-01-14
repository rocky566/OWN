import os
import json
from fbchat import Client
from fbchat.models import Message, ThreadType

# Load configuration from config.json
with open("config.json", "r") as f:
    config = json.load(f)

# Extract values from config
BOT_NAME = config["BOT_NAME"]
ADMIN_UID = config["ADMIN_UID"]

# Configuration for appstate file
APPSTATE_FILE = "appstate.json"  # Path to your appstate.json

# Function to generate appstate.json if it doesn't exist or is invalid
def generate_appstate():
    email = "YOUR_FACEBOOK_EMAIL"  # Replace with your Facebook email
    password = "YOUR_FACEBOOK_PASSWORD"  # Replace with your Facebook password
    
    client = Client(email, password)
    with open(APPSTATE_FILE, "w") as f:
        json.dump(client.getSession(), f)
    
    print(f"Session cookies saved to {APPSTATE_FILE}")
    client.logout()

# Check if appstate.json exists or is invalid
if not os.path.exists(APPSTATE_FILE):
    print(f"{APPSTATE_FILE} not found. Generating a new one...")
    generate_appstate()

# Load appstate.json
try:
    with open(APPSTATE_FILE, "r") as f:
        appstate = json.load(f)
except Exception as e:
    print(f"[ERROR]: Failed to load {APPSTATE_FILE}: {e}. Generating a new one...")
    generate_appstate()
    with open(APPSTATE_FILE, "r") as f:
        appstate = json.load(f)

# Initialize client with session cookies
try:
    client = Client(session_cookies=appstate)
    print(f"[{BOT_NAME}]: Logged in successfully as {client.uid}!")
except Exception as e:
    print(f"[ERROR]: Failed to log in using session cookies: {e}")
    raise

# Message Listener
class Bot(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        # Ignore bot's own messages
        if author_id == self.uid:
            return

        message_text = message_object.text or ""
        print(f"[MESSAGE]: Received from {author_id}: {message_text}")

        # Handle Commands
        if message_text.startswith("!"):  # Commands prefixed with "!"
            command = message_text[1:].strip().split()[0]  # Get the command
            if author_id == ADMIN_UID:
                if command == "hello":
                    self.send(Message(text="Hello, Admin!"), thread_id=thread_id, thread_type=thread_type)
                elif command == "stop":
                    self.send(Message(text="Stopping the bot..."), thread_id=thread_id, thread_type=thread_type)
                    print("[BOT]: Stopping...")
                    self.logout()
                else:
                    self.send(Message(text=f"Unknown command: {command}"), thread_id=thread_id, thread_type=thread_type)
            else:
                self.send(Message(text="You are not authorized to use commands!"), thread_id=thread_id, thread_type=thread_type)

# Start the bot
if __name__ == "__main__":
    bot = Bot(session_cookies=appstate)
    print(f"[{BOT_NAME}]: Bot is now running!")

    try:
        bot.listen()  # Start listening to messages
    except KeyboardInterrupt:
        print(f"[{BOT_NAME}]: Bot stopped by user.")
        bot.logout()
    except Exception as e:
        print(f"[ERROR]: An unexpected error occurred: {e}")
