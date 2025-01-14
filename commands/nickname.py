# commands/nickname.py

from fbchat.models import Message
from config import ADMIN_UID

def execute(client, author_id, message_text, thread_id, thread_type, **kwargs):
    if author_id != ADMIN_UID:
        client.send(Message(text="Only admin can set nickname!"), thread_id=thread_id, thread_type=thread_type)
        return

    nickname = message_text.split(" ", 1)[1] if len(message_text.split(" ", 1)) > 1 else "Unnamed"
    client.changeNickname(nickname, thread_id, author_id)
    client.send(Message(text=f"Nickname set to {nickname}"), thread_id=thread_id, thread_type=thread_type)
