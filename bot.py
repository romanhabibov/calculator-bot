#!/usr/bin/env python

import logging
import os
import sys

from telegram import ForceReply
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import Dispatcher
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import PicklePersistence
from telegram.ext import Updater

from calculator import calculate_expression


# Maximum message length in Telegram is 4096.
sys.setrecursionlimit(4096)
CACHE_SIZE = 5

# Enable logging.
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

class Cache():
    """Simple queue for caching the latest user commands."""

    def __init__(self):
        self.items = list()
        self.cache_size = CACHE_SIZE

    def add(self, item):
        """Add item to cache."""
        if len(self.items) == self.cache_size:
            self.items.pop(0)
        self.items.append(item)

    def print(self):
        """Print cache items."""
        return '\n'.join(self.items)

def load_cfg():
    """Generate config from environment variables."""

    cfg = dict()
    cfg['TOKEN'] = os.getenv('CB_TOKEN')
    if not cfg['TOKEN']:
        RuntimeError('CB_TOKEN didn\'t set.')
    cfg['MODE'] = os.getenv('CB_MODE')
    cfg['PORT'] = int(os.getenv('CB_PORT', '8443'))
    cfg['KEY'] = os.getenv('CB_KEY', 'private.key')
    cfg['CERT'] = os.getenv('CB_CERT', 'cert.pem')
    cfg['WEBHOOK_URL'] = os.getenv('CB_WEBHOOK_URL')

    return cfg

def start(update, context):
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi, {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True)
    )

def help_command(update, context):
    """Send a message when the command /help is issued."""

    help_text = 'This is the calculator bot. Send your '\
                'arithmetic expression and it answers with the result.\n'\
                'Supported operations: +, -, *, / and ().\n\n'\
                'Bot commands:\n/start - start bot.\n/help - for help.\n'\
                '/print_cache - show last 5 operations.'
    update.message.reply_text(help_text)

def print_cache(update, context):
    """Show cache of operations to user."""

    if context.user_data.get('cache'):
        update.message.reply_text(context.user_data.get('cache').print())

def error(update, context):
    """Log errors caused by Updater."""

    logger.warning('Update "%s" caused error "%s"', update, context.error)

def calculate(update, context):
    """Calculate the user's expression and send the result."""

    res = calculate_expression(update.message.text)
    update.message.reply_text(res)
    if not context.user_data.get('cache'):
        context.user_data['cache'] = Cache()
    item = 'Expression: "{0}" Result: "{1}"'.format(update.message.text, res)
    context.user_data['cache'].add(item)

def main():

    cfg = load_cfg()

    # Use pickle file to keep the cache of operations persistent.
    persistence = PicklePersistence(filename='cache')

    updater = Updater(cfg['TOKEN'], persistence=persistence)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("print_cache", print_cache))
    dispatcher.add_error_handler(error)

    # On non command i.e expression - answer with the result.
    msg_handler = MessageHandler(Filters.text & ~Filters.command, calculate)
    dispatcher.add_handler(msg_handler)

    url = 'https://{}/{}'.format(cfg['WEBHOOK_URL'], cfg['TOKEN'])
    if cfg.get('MODE') == 'webhook':
        list_parameters = {'listen': '0.0.0.0',
                           'port': int(cfg['PORT']),
                           'key': cfg.get('KEY'),
                           'cert': cfg.get('CERT'),
                           'url_path': cfg['TOKEN'],
                           'webhook_url': url}
        updater.start_webhook(list_parameters)
    else:
        updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives
    # SIGINT, SIGTERM or SIGABRT.
    updater.idle()

if __name__ == '__main__':
    main()
