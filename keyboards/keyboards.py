from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardBuilder
from utils.translation import *

from dotenv import dotenv_values
import os

dotenv = dotenv_values(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))


def creator_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Leave a message")],
            [KeyboardButton(text="Change messages")],
            [KeyboardButton(text="⬅️ BACK")]
            # [KeyboardButton(text="Stories")]
        ], resize_keyboard=True
    )

    return keyboard


def rus_messages_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Как добавить бота?")],
            [KeyboardButton(text="Список команд")],
            [KeyboardButton(text="О разработчике")],
            [KeyboardButton(text="⬅️ BACK")]
            # [KeyboardButton(text="Stories")]
        ], resize_keyboard=True
    )

    return keyboard


def eng_messages_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="How to add the bot")],
            [KeyboardButton(text="List of the commands")],
            [KeyboardButton(text="About dev")],
            [KeyboardButton(text="⬅️ BACK")]
            # [KeyboardButton(text="Stories")]
        ], resize_keyboard=True
    )

    return keyboard


def main_keyboard(language, user_id):

    builder = ReplyKeyboardBuilder()

    if user_id == int(dotenv['CREATOR_ID']):
        builder.row(KeyboardButton(text='🔐 FOR ADMINS'))

    builder.row(KeyboardButton(text=MESSAGES['instruction'][language]))
    builder.row(KeyboardButton(text=MESSAGES['command_list'][language]))
    builder.row(KeyboardButton(text=MESSAGES['report_a_bug'][language]))
    builder.row(KeyboardButton(text=MESSAGES['about_creator'][language]))
    builder.row(KeyboardButton(text=MESSAGES['change_language'][language]))

    return builder.as_markup(resize_keyboard=True)


def languages_buttons():
    languages = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🇷🇺 РУССКИЙ")],
            [KeyboardButton(text="🇬🇧 ENGLISH")]
        ], resize_keyboard=True
    )
    return languages


def lang_stories_buttons():
    languages = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="How to add the bot")],
            [KeyboardButton(text="List of commands")],
            [KeyboardButton(text="About me")],
            [KeyboardButton(text="When added to a group"),
             KeyboardButton(text="Applied photo")],
            [KeyboardButton(text="Welcome message")],
            [KeyboardButton(text="⬅️")]
        ], resize_keyboard=True
    )
    return languages


back = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="⬅️")]], resize_keyboard=True)


def cancel_button(language):
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text=f"{MESSAGES['cancel_button'][language]}"))
    return builder.as_markup(resize_keyboard=True)

# stories_rus = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="⬅️")], [KeyboardButton(text="Добавить ➕")]], resize_keyboard=True)
# stories_eng = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="⬅️")], [KeyboardButton(text="Add ➕")]], resize_keyboard=True)

# def russian_stories():
#     builder = ReplyKeyboardBuilder()
#     stories = get_all_rus_stories_titles()
#     [builder.button(text=story_title).adjust(2) for story_title in stories]
#     builder.row(KeyboardButton(text="Добавить ➕"))
#     builder.row(KeyboardButton(text="⬅️"))
#     return builder.as_markup(resize_keyboard=True)
#
#
# def english_stories():
#     builder = ReplyKeyboardBuilder()
#     stories = get_all_eng_stories_titles()
#     [builder.button(text=story_title).adjust(2) for story_title in stories]
#     builder.row(KeyboardButton(text="Add ➕"))
#     builder.row(KeyboardButton(text="⬅️"))
#     return builder.as_markup(resize_keyboard=True)