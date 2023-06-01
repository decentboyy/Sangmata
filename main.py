import logging
import telebot

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables
tracked_users = {}


bot = telebot.TeleBot("1719065252:AAH0y8WEkXrVdvH1ShG51PkC2SZEtLXVU40")


@bot.message_handler(commands=['start'])
def start(message):
    """Handler for the /start command."""
    bot.reply_to(message, "Hello! I will track name and username changes for you. "
                          "Add me to a group and give me admin rights to start tracking.")


@bot.message_handler(commands=['track'])
def track(message):
    """Handler for tracking name and username changes."""
    user = message.from_user

    if user.id in tracked_users:
        tracked_users[user.id]['name'] = user.full_name
        tracked_users[user.id]['username'] = user.username
    else:
        tracked_users[user.id] = {
            'name': user.full_name,
            'username': user.username
        }

    bot.reply_to(message, "You have been added to the tracking list.")


@bot.message_handler(content_types=['new_chat_members'])
def new_chat_member(message):
    """Handler for new chat members."""
    user = message.new_chat_member

    if user.id in tracked_users and user.full_name != tracked_users[user.id]['name']:
        text = f"🔔 Name Change Alert! 🔔\n\n"
        text += f"User: {user.full_name} ({user.id})\n"
        text += f"Old Name: {tracked_users[user.id]['name']}\n"
        text += f"New Name: {user.full_name}"

        bot.reply_to(message, text)
        tracked_users[user.id]['name'] = user.full_name


@bot.message_handler(func=lambda message: message.entities and any(entity.type in ['mention', 'text_mention'] for entity in message.entities))
def username_change(message):
    """Handler for username changes."""
    user = message.from_user
    user_id = user.id

    if user_id in tracked_users and user.username != tracked_users[user_id]['username']:
        text = f"🔔 Username Change Alert! 🔔\n\n"
        text += f"User: {user.full_name} ({user_id})\n"
        text += f"Old Username: {tracked_users[user_id]['username']}\n"
        text += f"New Username: {user.username}"

        bot.reply_to(message, text)
        tracked_users[user_id]['username'] = user.username


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    """Handler for other message types."""
    bot.reply_to(message, "I'm sorry, I only track name and username changes.")


@bot.message_handler(func=lambda message: True)
def error_handler(message):
    """Handler for errors."""
    logger.warning(f"Update {message} caused an error.")


# Start the bot
bot.polling()
