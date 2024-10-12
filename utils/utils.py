import configs
import re
import datetime

from dotenv import dotenv_values
import os

from pyrogram import Client
from pyrogram.raw.functions.contacts import ResolveUsername

config = dotenv_values(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))


def triggers(text, language):
    if language == "rus":
        if text:
            cleaned_text = re.sub(r'\s+', '', text.lower())
            for word in configs.SWEAR_WORDS_RUS:
                if re.search(rf"{word}", cleaned_text):
                    return True
    elif language == "eng":
        if text:
            cleaned_text = re.sub(r'\s+', '', text.lower())
            for word in configs.SWEAR_WORDS_ENG:
                if re.search(rf"{word}", cleaned_text):
                    return True
    return False


def banned_words(text, language):
    if language == "rus":
        if text:
            cleaned_text = re.sub(r'\s+', '', text.lower())
            for word in configs.BANNED_WORDS_RUS:
                if re.search(rf"{word}", cleaned_text):
                    return True
    elif language == "eng":
        if text:
            cleaned_text = re.sub(r'\s+', '', text.lower())
            for word in configs.BANNED_WORDS_ENG:
                if re.search(rf"{word}", cleaned_text):
                    return True
    return False


def for_gamerland(text):
    if text:
        cleaned_text = re.sub(r'\s+', '', text.lower())
        for word in configs.maxwell_ban:
            if re.search(rf"{word}", cleaned_text):
                return True
    return False


def time_converter(time_text) -> datetime:
    if not time_text:
        return None

    if time_text[-1] == 'ч':
        time_text_eng = time_text.replace("ч", "h")
        time_text = time_text_eng
    if time_text[-1] == 'м':
        time_text_eng = time_text.replace("м", "m")
        time_text = time_text_eng
    if time_text[-1] == 'д':
        time_text_eng = time_text.replace("д", "d")
        time_text = time_text_eng
    if time_text[-1] == 'н':
        time_text_eng = time_text.replace("н", "w")
        time_text = time_text_eng

    match_ = re.match(r"(\d+)([a-z])", time_text.lower().strip())

    current_time = datetime.datetime.now()

    if match_:
        value, unit = int(match_.group(1)), match_.group(2)

        match unit:
            case "m": time = datetime.timedelta(minutes=value)
            case "h": time = datetime.timedelta(hours=value)
            case "d": time = datetime.timedelta(days=value)
            case "w": time = datetime.timedelta(weeks=value)
            case _: return None

    else:
        return None

    new_datetime = current_time + time
    return new_datetime


def links_filter(text):
    url_pattern = re.compile(
        r'\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))'
    )
    exception = re.compile(r"^https://t\.me/Gamerlandbs$")

    if text:
        if not exception.search(text):
            if url_pattern.search(text):
                return True

    return False




# async def set_commands(bot: Bot):
#     await bot.delete_my_commands()  #switchable
#     commands = [
#     ]
#     await bot.set_my_commands(commands)
