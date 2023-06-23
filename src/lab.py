import requests

discord_webhook = ""

coin_img_dataset = {
    "BTC" : "https://s2.coinmarketcap.com/static/img/coins/64x64/1.png",
    "LTC" : "https://s2.coinmarketcap.com/static/img/coins/64x64/2.png",
    "DOGE" : "https://s2.coinmarketcap.com/static/img/coins/64x64/74.png",
    "ETH" : "https://s2.coinmarketcap.com/static/img/coins/64x64/1027.png",
    "XRP" : "https://s2.coinmarketcap.com/static/img/coins/64x64/52.png",
    "ADA" : "https://s2.coinmarketcap.com/static/img/coins/64x64/2010.png",
    "DOT" : "https://s2.coinmarketcap.com/static/img/coins/64x64/6636.png",
    "UNI" : "https://s2.coinmarketcap.com/static/img/coins/64x64/7083.png",
    "BCH" : "https://s2.coinmarketcap.com/static/img/coins/64x64/1831.png",
    "LINK" : "https://s2.coinmarketcap.com/static/img/coins/64x64/1975.png",
}
crypto_img_url = "https://blog.mexc.com/wp-content/uploads/2021/12/MX_Voting_MEXC_Token-768x527.png"

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
    requests.post(discord_webhook, json={"embeds": [embed],"avatar_url":"https://i.pinimg.com/564x/94/8d/38/948d38262a9cd80fbd7acad5ff43c56f.jpg","username":"Trading Bot"})
    return True

# Sends a test message and a test embed to the Discord webhook.
# send_discord_webhook_with_embed({"title": "test", "description": "test", "color": 0x00ff00})

order_recive_embed_template = {
    "title": "Order Recived",
    "description": "Sample Description",
    "color": 0x00ff00,
    "thumbnail": {
        "url": coin_img_dataset["BTC"]
    },
    "footer": {
        "text": "MEXC Global"
    },
    "fields": [
        {
            "name": "Symbol",
            "value": "BTCUSDT",
            "inline": True
        },
        {
            "name": "Side",
            "value": "Buy",
            "inline": True
        },
        {
            "name": "Quantity",
            "value": "0.001",
            "inline": True
        },
        {
            "name": "Price",
            "value": "10000",
            "inline": True
        },
        {
            "name": "Order Type",
            "value": "Limit",
            "inline": True
        },
        {
            "name": "Order ID",
            "value": "123456789",
            "inline": True
        },
        {
            "name": "Order Time",
            "value": "2021-01-01 00:00:00",
            "inline": True
        },
        {
            "name": "Order Status",
            "value": "Filled",
            "inline": True
        }
    ]
}

send_discord_webhook_with_embed(order_recive_embed_template)