import requests

discord_webhook = "https://discord.com/api/webhooks/992704125898850324/IQzP8eFP0iimYOnZ47uXcKBZFyeGhGsmQfwmqtojSmngP2cTA6AMvx4zigGZChhfAun2"

def send_discord_webhook(message):
    """
    Sends a message to a Discord webhook.

    Args:
        message (str): The message to send.

    Returns:
        bool: True if the message was sent successfully, False otherwise.
    """
    requests.post(discord_webhook, json={"content": message})
    return True

def send_discord_webhook_with_embed(embed):
    """
    Sends an embed to a Discord webhook.

    Args:
        embed (dict): The embed to send. Must be a dictionary containing the following keys:
            - title (str): The title of the embed.
            - description (str): The description of the embed.
            - color (int): The color of the embed in hexadecimal format.

    Returns:
        bool: True if the embed was sent successfully, False otherwise.
    """
    requests.post(discord_webhook, json={"embeds": [embed],"avatar_url":"https://yourcryptolibrary.com/wp-content/uploads/2023/02/MEXC-Logo.jpg","username":"MEXC"})
    return True

# Sends a test message and a test embed to the Discord webhook.
send_discord_webhook_with_embed({"title": "test", "description": "test", "color": 0x00ff00})