from telegram.ext.filters import Filters
from telegram import Update, message
from SaitamaRobot.modules.helper_funcs.chat_status import (
    bot_can_delete,
    connection_status,
    dev_plus,
    user_admin,
)
from SaitamaRobot import dispatcher
import html
from SaitamaRobot.modules.sql.antichannel_sql import antichannel_status, disable_antichannel, enable_antichannel
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    MessageHandler,
)
from SaitamaRobot.modules.helper_funcs.alternate import typing_action

@typing_action
@connection_status
@user_admin
def set_antichannel(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    args = context.args
    if len(args) > 0:
        s = args[0].lower()
        if s in ["yes", "on"]:
            enable_antichannel(chat.id)
            message.reply_html("Enabled antichannel in {}".format(html.escape(chat.title)))
        elif s in ["off", "no"]:
            disable_antichannel(chat.id)
            message.reply_html("Disabled antichannel in {}".format(html.escape(chat.title)))
        else:
            message.reply_text("Unrecognized arguments {}".format(s))
        return
    message.reply_html("Antichannel setting is currently {} in {}".format(antichannel_status(chat.id), html.escape(chat.title)))


def eliminate_channel(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    bot = context.bot
    if not antichannel_status(chat.id):
        return
    if message.sender_chat and message.sender_chat.type == "channel" and not message.is_automatic_forward:
        message.delete()
        sender_chat = message.sender_chat
        bot.ban_chat_sender_chat(sender_chat_id=sender_chat.id, chat_id=chat.id)


__help__ = """
Restrict users from sending as anonymous channels
 • `/antichannel <on/off/yes/no>`*:* enables antichannel in the current chat
If enabled, the message from the channel which the user sends will be banned.
"""

ANTICHANNEL_HANDLER = CommandHandler("antichannel", set_antichannel, run_async=True)
ELIMINATE_CHANNEL_HANDLER = MessageHandler(Filters.chat_type.groups, eliminate_channel, run_async=True)

dispatcher.add_handler(ANTICHANNEL_HANDLER)
dispatcher.add_handler(ELIMINATE_CHANNEL_HANDLER)
__mod_name__ = "Antichannel"

__handlers__ = [
    ANTICHANNEL_HANDLER,
    ELIMINATE_CHANNEL_HANDLER
    ]