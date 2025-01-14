# commands/help.py

from fbchat.models import Message

def execute(client, author_id, thread_id, thread_type, **kwargs):
    help_message = """
    Commands:
    - !help: Show this help message
    - !nickname <name>: Set custom nickname (admin only)
    """
    client.send(Message(text=help_message), thread_id=thread_id, thread_type=thread_type)
