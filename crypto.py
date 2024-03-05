import os
import requests
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import time


# Load environment variables from .env file
load_dotenv()

def send_email(subject, message):
    # Email configuration
    sender_email = os.getenv('SENDER_EMAIL')
    receiver_email = os.getenv('RECEIVER_EMAIL')
    password = os.getenv('EMAIL_PASSWORD')
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = int(os.getenv('SMTP_PORT'))
    # Compose email
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Connect to SMTP server and send email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender_email, password)
       smtp_server.sendmail(sender_email, receiver_email, msg.as_string())
    print("Message sent!")

def check_prices(coins):
    # Binance API endpoint for getting ticker prices for all coins
    url = 'https://api.binance.com/api/v3/ticker/price'

    # Make HTTP request to Binance API
    while True:
        # Make HTTP request to Binance API
        response = requests.get(url)
        data = response.json()

        # Check prices for each coin
        for coin in coins:
            symbol = coin['symbol']
            threshold = coin['threshold']
            for item in data:
                if item['symbol'] == symbol:
                    price = float(item['price'])
                    if price > threshold:
                        send_email(f'{symbol} Price Alert', f'{symbol} price has crossed {threshold}')

        # Wait for one second before checking again
        time.sleep(60)


# Example usage
if __name__ == "__main__":
    coins = [
        {'symbol': 'AVAXUSDT', 'threshold': 4000},   # Example: AVAX to USDT with threshold
        {'symbol': 'DOGEUSDT', 'threshold': 16},     # Example: DOGE to USDT with threshold
        {'symbol': 'FTMUSDT', 'threshold': 100},     # Example: FTM to USDT with threshold
        {'symbol': 'MANAUSDT', 'threshold': 110},    # Example: MANA to USDT with threshold
        {'symbol': '1INCHUSDT', 'threshold': 100},  # Example: 1INCH to USDT with threshold
        {'symbol': 'GALAUSDT', 'threshold': 10},    # Example: GALA to USDT with threshold
        {'symbol': 'MATICUSDT', 'threshold': 100},
        # Add more coins and their thresholds as needed
    ]
    check_prices(coins)
