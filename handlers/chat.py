from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext

from database.queries import *

from keyboards import keyboards as rp, inline as il

from utils.translation import MESSAGES

from filters.filters import *

from FSM.states import *

from dotenv import dotenv_values

dotenv = dotenv_values(".env")

CHANNEL_ID = int(dotenv['CHANNEL_LINK'])

rt = Router()


@rt.message(IsPrivateChat(), CommandStart())
async def command_start_handler(message: Message) -> None:
    if message.chat.id not in await get_all_chats():
        await insert_id(message.chat.id, f"USER: {message.from_user.full_name}")
        await message.answer(
            f"Hello, <b>{message.from_user.full_name}</b>\nChoose your language:\n\n"
            f"Приветствую тебя, <b>{message.from_user.full_name}</b>\nВыбери свой язык:", reply_markup=rp.languages_buttons())
    else:
        await message.answer("Добро пожаловать")


# @rt.callback_query(F.data == 'check_subscription')
# async def check_subscription(callback: CallbackQuery):
#     member = await callback.message.bot.get_chat_member(CHANNEL_ID, callback.message.from_user.id)
#
#     if member.status == 'left':
#         await callback.message.answer("Подпишитесь на канал перед тем, как начать использовать бота",
#                                         reply_markup=il.subscription_button)
#     else:
#         await command_start_handler(callback.message)


@rt.message(IsPrivateChat(), F.text.in_(["🇷🇺 РУССКИЙ", "🇬🇧 ENGLISH"]))
async def set_chat_language(message: Message):
    if message.text == "🇷🇺 РУССКИЙ":
        await insert_language('rus', message.chat.id)
    elif message.text == "🇬🇧 ENGLISH":
        await insert_language('eng', message.chat.id)
    language = await identify_language(message.chat.id)
    await message.answer(MESSAGES['welcome_user'][language], reply_markup=rp.main_keyboard(language, message.chat.id))


@rt.message(IsPrivateChat(), F.text.in_(["About the creator", "О создателе"]))
async def list_commands(message: Message):
    language = await identify_language(message.chat.id)
    about_dev = await get_about_dev()
    await message.answer(about_dev)


@rt.message(IsPrivateChat(), F.text.in_([
"Report a bug / Suggest an improvement",
"Сообщить об ошибке / Предложить улучшение"]))
async def bug_report(message: Message, state: FSMContext):
    language = await identify_language(message.chat.id)
    await state.set_state(BugReport.message)
    await message.answer(MESSAGES['bug_reported'][language], reply_markup=rp.cancel_button(language))


@rt.message(IsPrivateChat(), BugReport.message)
async def send_newsletter(message: Message, state: FSMContext, bot: Bot) -> None:
    language = await identify_language(message.chat.id)
    if message.text in list(MESSAGES['cancel_button'].values()):
        await message.answer(MESSAGES['cancelled_action'][language], reply_markup=rp.main_keyboard(language, message.chat.id))
        await state.clear()
    else:
        await message.answer(MESSAGES['waiting'][language])
        try:
            if message.from_user.username:
                await bot.send_message(chat_id=7215866709, text=f"<b>There is a message from @{message.from_user.username}!</b>")
            else:
                await bot.send_message(chat_id=7215866709, text=f"<b>There is a message from @{message.from_user.full_name}!</b>")
            await message.send_copy(chat_id=7215866709, reply_markup=il.admin_answer(message.from_user.id))
            await message.answer(MESSAGES['sending_success'][language], reply_markup=rp.main_keyboard(language, message.chat.id))
        except:
            await message.answer(MESSAGES['sending_error'][language], reply_markup=rp.main_keyboard(language, message.chat.id))
        await state.clear()


@rt.message(IsPrivateChat(), F.text.in_(["Add the bot to a group!", "Добавить бота в группу!"]))
async def add_me_instructions(message: Message):
    language = await identify_language(message.chat.id)
    how_to_add = await get_how_to_add()
    await message.answer(how_to_add)


@rt.message(IsPrivateChat(), F.text.in_(["List of the bot commands",
"Список команд бота"]))
async def list_commands(message: Message):
    language = await identify_language(message.chat.id)
    list_of_command = await get_commands_list()
    await message.answer(list_of_command)


@rt.message(IsPrivateChat(), F.text.in_(["Change language", "Изменить язык"]))
async def switch_languages(message: Message):
    await message.answer(
        f"Hello, <b>{message.from_user.full_name}</b>\nChoose your language:\n\n"
        f"Приветствую тебя, <b>{message.from_user.full_name}</b>\nВыбери свой язык:",
        reply_markup=rp.languages_buttons())


@rt.message(IsPrivateChat(), F.text.in_(list(MESSAGES["back_button"].values())))
async def back_to_main_menu(message: Message):
    language = await identify_language(message.chat.id)
    await message.answer(MESSAGES['back_to_main_menu'][language], reply_markup=rp.main_keyboard(language, message.chat.id))