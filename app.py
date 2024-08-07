import os
import instaloader
import telebot
import logging


# Set the TELEGRAM_BOT_TOKEN environment variable
# Retrieve the Telegram bot token from environment variables
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')

if not bot_token:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable not found.")

bot = telebot.TeleBot(bot_token)
loader = instaloader.Instaloader()

# handle the "/start" command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Welcome to my Instagram bot! Send me a username or profile share url to get their profile picture.')

@bot.message_handler(func=lambda message: True)
def get_profile_picture(message):
    text = message.text.strip()
    if text.startswith('https://www.instagram.com/'):
        username = text.replace('https://www.instagram.com/', '').split('?')[0].rstrip('/')
    else:
        username = text
    try:
        profile = instaloader.Profile.from_username(loader.context, username)
        profile_pic_url = profile.profile_pic_url
        bot.send_photo(message.chat.id, photo=profile_pic_url)

    except instaloader.exceptions.ProfileNotExistsException:
        bot.reply_to(message, "Instagram profile not found. Please check the username.")
    except Exception as e:
        logging.warning(message, f"An error occurred: {e}")
        bot.reply_to(message,"Sorry!! Couldn't find the profile you are looking for, send a valid Profile.")

bot.polling()
