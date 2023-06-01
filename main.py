import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables
tracked_users = {}


def start(update: Update, _) -> None:
    """Handler for the /start command."""
    update.message.reply_text("Hello! I will track name and username changes for you. "
                              "Add me to a group and give me admin rights to start tracking.")


def track(update: Update, _) -> None:
    """Handler for tracking name and username changes."""
    user = update.message.from_user

    if user.id in tracked_users:
        tracked_users[user.id]['name'] = user.full_name
        tracked_users[user.id]['username'] = user.username
    else:
        tracked_users[user.id] = {
            'name': user.full_name,
            'username': user.username
        }

    update.message.reply_text("You have been added to the tracking list.")


def notify_name_change(update: Update, _) -> None:
    """Handler for name changes."""
    user = update.message.from_user
    user_id = user.id

    if user_id in tracked_users and user.full_name != tracked_users[user_id]['name']:
        text = f"🔔 Name Change Alert! 🔔\n\n"
        text += f"User: {user.full_name} ({user_id})\n"
        text += f"Old Name: {tracked_users[user_id]['name']}\n"
        text += f"New Name: {user.full_name}"

        update.message.reply_text(text)
        tracked_users[user_id]['name'] = user.full_name


def notify_username_change(update: Update, _) -> None:
    """Handler for username changes."""
    user = update.message.from_user
    user_id = user.id

    if user_id in tracked_users and user.username != tracked_users[user_id]['username']:
        text = f"🔔 Username Change Alert! 🔔\n\n"
        text += f"User: {user.full_name} ({user_id})\n"
        text += f"Old Username: {tracked_users[user_id]['username']}\n"
        text += f"New Username: {user.username}"

        update.message.reply_text(text)
        tracked_users[user_id]['username'] = user.username


def error(update: Update, context) -> None:
    """Log errors."""
    logger.warning(f"Update {update} caused error {context.error}")


def main() -> None:
    """Start the bot."""
    # Set up the Telegram Bot
    updater = Updater("1719065252:AAH0y8WEkXrVdvH1ShG51PkC2SZEtLXVU40")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("track", track))
    dispatcher.add_handler(MessageHandler(Filters.entity("bold") | Filters.entity("italic"), notify_name_change))
    dispatcher.add_handler(MessageHandler(Filters.username, notify_username_change))
    dispatcher.add_error_handler(error)

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()


if __name__ == '__main__':
    main()
