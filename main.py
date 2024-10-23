
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
import threading
import time
import psutil
from datetime import datetime
import os

# Your bot token from @BotFather (consider using environment variables for security)
TOKEN = '6293447468:AAHlxvdm0kQKR4aU2VFWENTB_4x4fDd4mjY'

# Initialize bot with token
bot = telebot.TeleBot(TOKEN)

# List of URLs to ping
urls = ["https://stp-advance.onrender.com"]

# Dictionary to track if we are waiting for a URL input per user
awaiting_url = {}

def get_system_details():
    try:
        public_ip = requests.get('https://ifconfig.me').text.strip()
    except requests.RequestException:
        public_ip = 'Unavailable'

    try:
        cpu_count = psutil.cpu_count(logical=False)
        logical_cpu_count = psutil.cpu_count(logical=True)
        cpu_freq = psutil.cpu_freq().current

        ram_info = psutil.virtual_memory()
        total_ram = ram_info.total / (1024 ** 3)
        available_ram = ram_info.available / (1024 ** 3)

        current_process = psutil.Process()
        thread_count = current_process.num_threads()
    except Exception as e:
        cpu_count = logical_cpu_count = cpu_freq = total_ram = available_ram = thread_count = 'Unavailable'
        print(f"Error fetching system details: {e}")

    system_details = {
        "public_ip": public_ip,
        "current_time_ist": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "cpu_info": {
            "physical_cores": cpu_count,
            "logical_cores": logical_cpu_count,
            "current_frequency_mhz": cpu_freq
        },
        "ram_info": {
            "total_ram_gb": f"{total_ram:.2f} GB" if total_ram != 'Unavailable' else total_ram,
            "available_ram_gb": f"{available_ram:.2f} GB" if available_ram != 'Unavailable' else available_ram
        },
        "thread_info": {
            "thread_count": thread_count
        }
    }

    return system_details

# Function to ping URLs
def ping_urls():
    while True:
        for url in urls:
            try:
                response = requests.get(url)
                print(f"URL: {url}, Status Code: {response.status_code}, Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            except requests.exceptions.RequestException as e:
                print(f"Failed to reach {url}. Reason: {e}")
        time.sleep(50)  # Ping every 50 seconds

# Function to display the inline keyboard
def main_menu(chat_id):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("Add URL", callback_data="add_url"),
        InlineKeyboardButton("View URLs", callback_data="view_urls")
    )
    bot.send_message(chat_id, "Choose an action:", reply_markup=markup)

# Start command handler
@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id
    system_info = get_system_details()
    bot.send_message(chat_id, f"Welcome! This is your URL management bot.\n\nSystem Details:\n{system_info}")
    main_menu(chat_id)

# Handler for inline keyboard button clicks
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    chat_id = call.message.chat.id
    if call.data == "add_url":
        awaiting_url[chat_id] = True  # Set a flag that we're awaiting a URL input
        bot.send_message(chat_id, "Please send me the URL to add.")
    elif call.data == "view_urls":
        urls_list = '\n'.join(urls) if urls else "No URLs have been added yet."
        bot.send_message(chat_id, f"Current URLs:\n{urls_list}")
    main_menu(chat_id)

# Handler for receiving messages (to capture new URLs)
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id

    # If the bot is awaiting a URL input, process the message
    if awaiting_url.get(chat_id):
        new_url = message.text.strip()
        if new_url.startswith("http://") or new_url.startswith("https://"):
            urls.append(new_url)
            bot.send_message(chat_id, f"URL '{new_url}' added successfully!")
        else:
            bot.send_message(chat_id, "Invalid URL format. Please start with 'http://' or 'https://'.")
        
        # Reset the flag after URL is received
        awaiting_url[chat_id] = False
        main_menu(chat_id)
    else:
        bot.send_message(chat_id, "Please use the menu to interact with the bot.")

# Function to start the pinging process in a separate thread
def start_pinging():
    ping_thread = threading.Thread(target=ping_urls)
    ping_thread.daemon = True
    ping_thread.start()

# Main function to start the bot
if __name__ == "__main__":
    if TOKEN is None:
        print("Error: TELEGRAM_BOT_TOKEN environment variable is not set.")
    else:
        start_pinging()  # Start the URL pinging thread
        bot.polling()
