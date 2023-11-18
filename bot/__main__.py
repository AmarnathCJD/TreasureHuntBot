from . import bot, BOT_TOKEN

bot.start(bot_token=BOT_TOKEN)

from .util import module_loader

# (c) @RoseLoverX

module_loader()

bot.run_until_disconnected()
