from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def languages_inline_buttons():
    languages = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🇷🇺 РУССКИЙ", callback_data="rus")],
            [InlineKeyboardButton(text="🇬🇧 ENGLISH", callback_data="eng")]
        ]
    )
    return languages


delete_rus = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="❌", callback_data="delr")]])
delete_eng = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="❌", callback_data="dele")]])


def admin_answer(sender_id):
    button = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Answer the message",
                                                                         callback_data=f"answer_to_{sender_id}")]])

    return button


subscription_button = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="ПОДПИСАТЬСЯ НА КАНАЛ АВТОРА", url="https://t.me/hikkiprods")]])