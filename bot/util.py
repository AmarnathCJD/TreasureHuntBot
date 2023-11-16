from . import bot
from telethon import events
import logging
from os import path, listdir

LOG = logging.getLogger("bot.util")


def new_cmd(**args):
    args["pattern"] = "(?i)^[!/-]" + args["pattern"] + "(?: |$)(.*)"

    def decorator(func):
        async def wrapper(event):
            await func(event)

        bot.add_event_handler(wrapper, events.NewMessage(**args))
        return func

    return decorator


def new_inline(**args):
    def decorator(func):
        async def wrapper(event):
            await func(event)

        bot.add_event_handler(wrapper, events.CallbackQuery(**args))
        return func

    return decorator


def module_loader():
    from pathlib import Path
    import importlib
    import sys

    for file in listdir(path.dirname(__file__) + "/modules"):
        name = "bot.modules." + Path(file).stem
        if "__" in name:
            continue
        importlib.import_module(name)
        sys.modules[name].module_loader = module_loader
        LOG.info(f"Loaded module {name}")
