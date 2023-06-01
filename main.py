from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables
tracked_users = {}


def start(update, context):
    """Handler for the /start command."""
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I will track name and username changes for you. "
                                                                    "Add me to a group and give me admin rights to start tracking.")


def track(update, context):
    """Handler for tracking name and username changes."""
    user = update.effective_user

    if user.id in tracked_users:
        tracked_users[user.id]['name'] = user.full_name
        tracked_users[user.id]['username'] = user.username
    else:
        tracked_users[user.id] = {
            'name': user.full_name,
            'username': user.username
        }

    context.bot.send_message(chat_id=update.effective_chat.id, text="You have been added to the tracking list.")


def new_chat_member(update, context):
    """Handler for new chat members."""
    user = update.message.new_chat_members[0]

    if user.id in tracked_users and user.full_name != tracked_users[user.id]['name']:
        text = f"🔔 Name Change Alert! 🔔\n\n"
        text += f"User: {user.full_name} ({user.id})\n"
        text += f"Old Name: {tracked_users[user.id]['name']}\n"
        text += f"New Name: {user.full_name}"

        context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        tracked_users[user.id]['name'] = user.full_name


def username_change(update, context):
    """Handler for username changes."""
    user = update.effective_user

    if user.id in tracked_users and user.username != tracked_users[user.id]['username']:
        text = f"🔔 Username Change Alert! 🔔\n\n"
        text += f"User: {user.full_name} ({user.id})\n"
        text += f"Old Username: {tracked_users[user.id]['username']}\n"
        text += f"New Username: {user.username}"

        context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        tracked_users[user.id]['username'] = user.username


def echo_all(update, context):
    """Handler for other message types."""
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm sorry, I only track name and username changes.")


def error_handler(update, context):
    """Handler for errors."""
    logger.warning(f"Update {update} caused an error.")


def main():
    """Main function to run the bot."""
    # Create the Updater and pass your bot token
    updater = Updater(token="1719065252:AAH0y8WEkXrVdvH1ShG51PkC2SZEtLXVU40", use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("track", track))
    dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_chat_member))
    dispatcher.add_handler(MessageHandler(Filters.user, username_change))
    dispatcher.add_handler(MessageHandler(Filters.all, echo_all))

    # Log errors
    dispatcher.add_error_handler(error_handler)

    # Start the bot
    updater.start_polling()

    # Run the bot until Ctrl+C is pressed
    updater.idle()


if __name__ == '__main__':
    main()
