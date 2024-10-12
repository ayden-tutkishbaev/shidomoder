import asyncio

from aiogram import Router, Bot, F
from aiogram.filters import Command, CommandObject, CommandStart, or_f, ChatMemberUpdatedFilter
from aiogram.types import ChatPermissions, CallbackQuery, ChatMemberUpdated

from utils.utils import *
from database.queries import *
from utils.translation import *

import random

import os
from dotenv import dotenv_values
import google.generativeai as genai

from contextlib import suppress

from aiogram.exceptions import TelegramBadRequest, TelegramNotFound

from mptroto import get_chat_members

from keyboards import inline as il

from filters.filters import *

rt = Router()

dotenv = dotenv_values(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))
genai.configure(api_key=dotenv['AI_TOKEN'])


@rt.message(IsGroupChat(),  Command(commands=['стартгруппы', 'startgroup']))
async def command_start_handler(message: Message, bot: Bot) -> None:
    chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if chat_member.status not in ['administrator', 'creator'] and not message.sender_chat:
        await message.answer("🛡 <i>Error: Access prohibited!</i>")
    else:
        chat_id = message.chat.id
        group_title = message.chat.title
        chat_members = await get_chat_members(message.chat.id)
        for chat_member in chat_members:
            try:
                await insert_all_members_to_chat(chat_id=message.chat.id, chat_name=message.chat.title,
                                                 user_id=chat_member['user_id'], user_name=chat_member['first_name'])
            except:
                pass
        await insert_id(chat_id, f"GROUP: {message.chat.full_name}")
        await insert_id_to_chat_permissions(chat_id, group_title)
        await message.answer(
            f"Hello, members of «<b>{message.chat.title}</b>» group\nChoose your language:\n\n"
            f"Приветствую всех участников чата «<b>{message.chat.title}</b>»\nВыберите свой язык:",
            reply_markup=il.languages_inline_buttons())


@rt.chat_member(ChatMemberUpdatedFilter(member_status_changed=F.member.status == "member"))
async def on_bot_added_to_group(event: ChatMemberUpdated, bot: Bot):
    if event.new_chat_member.user.id == (await bot.me()).id:
        await bot.send_message(event.chat.id, "всем привет")


@rt.message(Command('testmessage'))
async def test_message(message: Message):
    permits = await get_chat_permissions(message.chat.id)
    print(permits)



@rt.message(or_f(F.text.casefold().startswith("how dumb i am"), F.text.casefold().startswith("how dumb"),
                 F.text.casefold().startswith("насколько я тупой"), F.text.casefold().startswith("насколько тупой"),
                 F.text.casefold().startswith("я тупой на")))
async def cmd_all_members(message: Message, bot: Bot):
    language = await identify_language(message.chat.id)
    if language == "rus":
        await message.answer(f"😵‍💫 <b>{message.from_user.full_name}</b>, <i>ты тупой на</i> <b>{random.randrange(0, 100)}%</b>!")
    if language == "eng":
        await message.answer(f"😵‍💫 <b>{message.from_user.full_name}</b>, <i>you are</i> <b>{random.randrange(0, 100)}%</b> dumb!")


@rt.message(IsGroupChat(), Command(commands=['rules', 'правила']))
async def rules_of_chat(message: Message):
    data = await get_chat_rules(message.chat.id)
    await message.answer(data)


@rt.message(IsGroupChat(), Command(commands=['изменитьправила', 'changerules']))
async def change_rules_of_chat(message: Message, command: CommandObject):
    await set_rules(command.args, message.chat.id)
    await message.answer("Правила изменены!\n\nRules have been changed!")


@rt.message(IsGroupChat(), Command(commands=['расписание', 'timetable']))
async def change_rules_of_chat(message: Message, command: CommandObject):
    await set_timetable(command.args, message.chat.id)
    await message.answer("Расписание чата изменено!\n\nThe chat's timetable has been changed")


@rt.chat_member(F.new_chat_member.status == "member")
async def on_new_chat_member(event: ChatMemberUpdated, bot: Bot):
    new_user = event.new_chat_member.user
    chat_id = event.chat.id
    language = await identify_language(chat_id)

    greeting_message = f'🤗 <b>{event.from_user.mention_html(new_user.full_name)}</b>, <i>{MESSAGES["welcome1"][language]}</i> <b>{event.from_user.mention_html(event.chat.title)}</b>!\n\n<i><b>{MESSAGES["welcome2"][language]}</b></i>'

    await insert_all_members_to_chat(chat_id=event.chat.id, chat_name=event.chat.title,
                                     user_id=new_user.id, user_name=new_user.first_name)

    # Отправляем сообщение в группу
    await bot.send_message(chat_id=chat_id, text=greeting_message)


@rt.message(IsGroupChat(), Command(commands=['links', 'ссылки']))
async def permissions_menu(message: Message, bot: Bot):
    language = await identify_language(message.chat.id)
    chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if chat_member.status not in ['administrator', 'creator'] and not message.sender_chat:
        await message.answer(MESSAGES['admin_rights_prohibited'][language])
    else:
        await on_links(message.chat.id)
        await message.answer(MESSAGES['links_on'][language])


@rt.message(IsGroupChat(), Command(commands=["antilinks", "безссылок"]))
async def permissions_menu(message: Message, bot: Bot):
    language = await identify_language(message.chat.id)
    chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if chat_member.status not in ['administrator', 'creator'] and not message.sender_chat:
        await message.answer(MESSAGES['admin_rights_prohibited'][language])
    else:
        await off_links(message.chat.id)
        await message.answer(MESSAGES['links_off'][language])


@rt.message(IsGroupChat(), Command(commands=["adultschat", "взрослый"]))
async def permissions_menu(message: Message, bot: Bot):
    language = await identify_language(message.chat.id)
    chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if chat_member.status not in ['administrator', 'creator'] and not message.sender_chat:
        await message.answer(MESSAGES['admin_rights_prohibited'][language])
    else:
        await on_swears(message.chat.id)
        await message.answer(MESSAGES['strong_language_on'][language])


@rt.message(IsGroupChat(), Command(commands=["familychat", "семейный"]))
async def permissions_menu(message: Message, bot: Bot):
    language = await identify_language(message.chat.id)
    chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if chat_member.status not in ['administrator', 'creator'] and not message.sender_chat:
        await message.answer(MESSAGES['admin_rights_prohibited'][language])
    else:
        await off_swears(message.chat.id)
        await message.answer(MESSAGES['strong_language_off'][language])


# @rt.message(IsGroupChat(), lambda message: message.text in ["Шидо расскажи историю", "Shido tell a story"])
# async def dushnila_shido(message: Message):
#     language = await identify_language(message.chat.id)
#     await message.answer(MESSAGES['dushnila'][language])
#
#
# @rt.message(IsGroupChat(), lambda message: message.text in ["Шидо, расскажи историю", "Shido, tell a story"])
# async def shido_tells_a_story(message: Message):
#     language = identify_language(message.chat.id)
#     if language == "eng":
#         story = get_eng_story(random.choice(get_all_eng_stories_ids()))
#         await message.answer(f"<b>{story[0]}</b>\n\n{story[1]}")
#     elif language == "rus":
#         story = get_rus_story(random.choice(get_all_rus_stories_ids()))
#         await message.answer(f"<b>{story[0]}</b>\n\n{story[1]}")


@rt.message(IsGroupChat(), Command(commands=['language', 'язык']))
async def set_bot_language(message: Message, bot: Bot) -> None:
    chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if chat_member.status not in ['administrator', 'creator'] and not message.sender_chat:
        await message.answer("🛡 <i>Error: Access prohibited!</i>")
    else:
        await message.answer(
            f"Hello, members of <b>{message.chat.title}</b> chat!\nChoose a language on which I will be operated.\n:)",
            reply_markup=il.languages_inline_buttons())


@rt.callback_query(CallGroupChat(), lambda callback: callback.data in ["rus", "eng"])
async def set_message(callback: CallbackQuery, bot: Bot):
    chat_member = await bot.get_chat_member(callback.message.chat.id, callback.message.from_user.id)
    await insert_language(callback.data, callback.message.chat.id)
    language = await identify_language(callback.message.chat.id)
    await callback.message.delete()
    welcome_message = await get_welcome_message()
    applied_photo = await get_addition_photo()
    first_message = await get_addition_to_a_group()
    await callback.message.answer_photo(caption=first_message, photo=applied_photo)
    await callback.message.answer(welcome_message)


@rt.message(IsGroupChat(), Command(commands=["mute", "мут"])) # TODO: fix
async def mute_handler(message: Message, bot: Bot, command: CommandObject):
    chat_id = message.chat.id
    language = await identify_language(chat_id)
    chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)

    reply = message.reply_to_message
    if not reply:
        if chat_member.status not in ['administrator', 'creator'] and not message.sender_chat:
            return await message.answer(MESSAGES['admin_rights_prohibited'][language])
        else:
            return await message.answer(MESSAGES['reply_to_restrict'][language])

    until_date = time_converter(command.args)

    if chat_member.status not in ['administrator', 'creator'] and not message.sender_chat:
        return await message.answer(MESSAGES['admin_rights_prohibited'][language])

    if command.args:
        reason_filter = command.args.split(" ")
        reason = " ".join(reason_filter[1:])
    else:
        reason_filter = []
        reason = ""

    with suppress(TelegramBadRequest):
        await bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=reply.from_user.id,
            permissions=ChatPermissions(can_send_messages=False),
            until_date=until_date
        )
        if reason == "":
            await message.answer(f"🚫 <b>{reply.from_user.mention_html(reply.from_user.first_name)}</b> {MESSAGES['muted_no_reason'][language]}!")
        else:
            await message.answer(f"🚫 <b>{reply.from_user.mention_html(reply.from_user.first_name)}</b> {MESSAGES['muted'][language]} <b>{reason}</b>!")


@rt.message(IsGroupChat(), or_f(F.text.casefold() == 'аура', F.text.casefold() == 'aura'))
async def users_karma(message: Message):
    language = await identify_language(message.chat.id)
    karma = await check_users_karma(user_id=message.from_user.id, chat_id=message.chat.id)
    await message.reply(f"✨ <b>{MESSAGES['users_karma'][language]}</b>{karma}")


@rt.message(IsGroupChat(), F.text.in_(['+', '👍']))
async def users_karma_increase(message: Message):
    language = await identify_language(message.chat.id)
    if message.reply_to_message:
        if message.reply_to_message.from_user.id != message.from_user.id:
            received_karma = await check_users_karma(user_id=message.reply_to_message.from_user.id, chat_id=message.chat.id)
            new_karma = received_karma + 1
            karma_sender = await check_users_karma(user_id=message.from_user.id, chat_id=message.chat.id)
            await insert_new_karma(user_id=message.reply_to_message.from_user.id, chat_id=message.chat.id, karma=new_karma)
            await message.answer(f"😇 {message.from_user.full_name} ({karma_sender}) <b>{MESSAGES['karma_increased'][language]}</b> {message.reply_to_message.from_user.full_name} ({new_karma})")
        else:
            await message.answer(f"<b>{MESSAGES['self_karma'][language]}</b>")


@rt.message(IsGroupChat(), F.text.in_(['-', '👎']))
async def users_karma_decrease(message: Message):
    language = await identify_language(message.chat.id)
    if message.reply_to_message:
        if message.reply_to_message.from_user.id != message.from_user.id:
            received_karma = await check_users_karma(user_id=message.reply_to_message.from_user.id, chat_id=message.chat.id)
            new_karma = received_karma - 1
            karma_sender = await check_users_karma(user_id=message.from_user.id, chat_id=message.chat.id)
            await insert_new_karma(user_id=message.reply_to_message.from_user.id, chat_id=message.chat.id, karma=new_karma)
            await message.answer(f"😕 {message.from_user.full_name} ({karma_sender}) <b>{MESSAGES['karma_decreased'][language]}</b> {message.reply_to_message.from_user.full_name} ({new_karma})")
        else:
            await message.answer(f"<b>{MESSAGES['self_karma'][language]}</b>")


#########################################################################################################
@rt.message(IsGroupChat(), Command(commands=["unmute", "размут"]))
async def mute_handler(message: Message, bot: Bot):
    chat_id = message.chat.id
    language = await identify_language(chat_id)
    chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    reply = message.reply_to_message

    if chat_member.status not in ['administrator', 'creator'] and not message.sender_chat:
        await message.answer(MESSAGES['admin_rights_prohibited'][language])
    else:
        if not reply:
            return await message.answer(MESSAGES['reply_to_restrict'][language])
        else:
            with suppress(TelegramBadRequest):
                await bot.restrict_chat_member(
                    chat_id=message.chat.id,
                    user_id=reply.from_user.id,
                    permissions=ChatPermissions(
                        can_send_messages=True,
                        can_send_photos=True,
                        can_send_videos=True,
                        can_send_documents=True,
                        can_send_other_messages=True,
                        can_send_audios=True,
                        can_send_video_notes=True,
                        can_send_voice_notes=True,
                        can_invite_users=True,
                        can_send_polls=True,
                        can_add_web_page_previews=True
                    ),
                    until_date=None
                )
                await message.answer(
                    f"😌 <b>{reply.from_user.mention_html(reply.from_user.first_name)}</b> {MESSAGES['unmute'][language]}")


@rt.message(IsGroupChat(), Command(commands=["ban", "бан"]))   # TODO: fix
async def mute_handler(message: Message, bot: Bot, command: CommandObject):
    language = await identify_language(message.chat.id)
    chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)

    reply = message.reply_to_message
    if not reply:
        if chat_member.status not in ['administrator', 'creator'] and not message.sender_chat:
            return await message.answer(MESSAGES['admin_rights_prohibited'][language])
        else:
            return await message.answer(MESSAGES['reply_to_restrict'][language])

    if chat_member.status not in ['administrator', 'creator'] and not message.sender_chat:
        return await message.answer(MESSAGES['admin_rights_prohibited'][language])

    if command.args:
        reason_filter = command.args.split(" ")
        reason = " ".join(reason_filter)
    else:
        reason_filter = []
        reason = ""

    with suppress(TelegramBadRequest):
        await bot.ban_chat_member(chat_id=message.chat.id, user_id=reply.from_user.id)
        if reason == "":
            await message.answer(f"❌ <b>{reply.from_user.mention_html(reply.from_user.first_name)}</b> {MESSAGES['banned_no_reason'][language]}!")
        else:
            await message.answer(f"❌ <b>{reply.from_user.mention_html(reply.from_user.first_name)}</b> {MESSAGES['banned'][language]} <b>{reason}</b>!")


@rt.message(IsGroupChat(), Command(commands=["unban", "разбан"]))
async def unban_handler(message: Message, bot: Bot) -> None:
    reply = message.reply_to_message
    language = await identify_language(message.chat.id)
    chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if chat_member.status not in ['administrator', 'creator'] and not message.sender_chat:
        await message.answer(MESSAGES['admin_rights_prohibited'][language])
    else:
        if not reply:
            await message.answer(MESSAGES['reply_to_restrict'][language])
        else:
            suspect = await bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
            if suspect.status not in ['kicked']:
                await message.answer(f"😳 {reply.from_user.mention_html(reply.from_user.first_name)} {MESSAGES['unban_error'][language]}")
            else:
                with suppress(TelegramBadRequest):
                    await bot.unban_chat_member(chat_id=message.chat.id, user_id=reply.from_user.id)
                    await message.answer(
                        f"🔓 {reply.from_user.mention_html(reply.from_user.first_name)} {MESSAGES['unban'][language]}")


@rt.message(IsGroupChat(), or_f(F.text.casefold().startswith("hug"), F.text.casefold().startswith("обнять")))
async def hug_handler(message: Message, bot: Bot):
    reply = message.reply_to_message
    if reply:
        language = await identify_language(message.chat.id)
        quote = ' '.join(message.text.split(' ')[1:])
        if reply.from_user.id == 6716078059:
            if quote == '':
                await message.reply(f"🫂 <b>{message.from_user.mention_html(message.from_user.full_name)}</b> <i>{MESSAGES['bot_hugged'][language]}</i>")
            else:
                await message.reply(f"🫂 <b>{message.from_user.mention_html(message.from_user.full_name)}</b> <i>{MESSAGES['bot_hugged'][language]}</i>\n\n<i>{quote}</i>\n- {message.from_user.full_name}")
        elif reply.from_user.id == message.from_user.id:
            pass
        else:
            if quote == '':
                await message.reply(f"🫂 <b>{message.from_user.mention_html(message.from_user.full_name)}</b> <i>{MESSAGES['hugs_message'][language]}</i> <b>{reply.from_user.mention_html(reply.from_user.full_name)}</b>")
            else:
                await message.reply(f"🫂 <b>{message.from_user.mention_html(message.from_user.full_name)}</b> <i>{MESSAGES['hugs_message'][language]}</i> <b>{reply.from_user.mention_html(reply.from_user.full_name)}</b>\n\n<i>{quote}</i>\n- {message.from_user.full_name}")


@rt.message(IsGroupChat(), or_f(F.text.casefold().startswith("kiss"), F.text.casefold().startswith("поцеловать"), F.text.casefold().startswith("чмок")))
async def kiss_handler(message: Message):
    reply = message.reply_to_message
    if reply:
        language = await identify_language(message.chat.id)
        quote = ' '.join(message.text.split(' ')[1:])
        if reply.from_user.id == 6716078059:
            if quote == '':
                await message.reply(f"💋 <b>{message.from_user.mention_html(message.from_user.full_name)}</b> <i>{MESSAGES['bot_kissed'][language]}</i>")
            else:
                await message.reply(f"💋 <b>{message.from_user.mention_html(message.from_user.full_name)}</b> <i>{MESSAGES['bot_kissed'][language]}</i>\n\n<i>{quote}</i>\n- {message.from_user.full_name}")
        elif reply.from_user.id == message.from_user.id:
            pass
        else:
            if quote == '':
                await message.reply(f"💋 <b>{message.from_user.mention_html(message.from_user.full_name)}</b> <i>{MESSAGES['kiss_message'][language]}</i> <b>{reply.from_user.mention_html(reply.from_user.full_name)}</b>")
            else:
                await message.reply(f"💋 <b>{message.from_user.mention_html(message.from_user.full_name)}</b> <i>{MESSAGES['kiss_message'][language]}</i> <b>{reply.from_user.mention_html(reply.from_user.full_name)}</b>\n\n<i>{quote}</i>\n- {message.from_user.full_name}")


@rt.message(IsGroupChat(), or_f(F.text.casefold().startswith("убить"), F.text.casefold().startswith("kill")))
async def kill_handler(message: Message):
    reply = message.reply_to_message
    if reply:
        language = await identify_language(message.chat.id)
        quote = ' '.join(message.text.split(' ')[1:])
        if reply.from_user.id == 6716078059:
            if quote == '':
                await message.reply(f"👻 <b>{message.from_user.mention_html(message.from_user.full_name)}</b> <i>{MESSAGES['bot_killed'][language]}</i>")
            else:
                await message.reply(f"👻 <b>{message.from_user.mention_html(message.from_user.full_name)}</b> <i>{MESSAGES['bot_killed'][language]}</i>")
        elif reply.from_user.id == message.from_user.id:
            pass
        else:
            if quote == '':
                await message.reply(f"😵 <b>{message.from_user.mention_html(message.from_user.full_name)}</b> <i>{MESSAGES['kill_message'][language]}</i> <b>{reply.from_user.mention_html(reply.from_user.full_name)}</b>")
            else:
                await message.reply(f"😵 <b>{message.from_user.mention_html(message.from_user.full_name)}</b> <i>{MESSAGES['kill_message'][language]}</i> <b>{reply.from_user.mention_html(reply.from_user.full_name)}</b>\n\n<i>{quote}</i>\n- {message.from_user.full_name}")


@rt.message(IsGroupChat(), or_f(F.text.casefold().startswith("пожать руку"), F.text.casefold().startswith("shake hand"), F.text.casefold().startswith("handshake")))
async def handshake_handler(message: Message):
    reply = message.reply_to_message
    if reply:
        language = await identify_language(message.chat.id)
        quote = ' '.join(message.text.split(' ')[1:]) if message.text.casefold().startswith("handshake") else ' '.join(message.text.split(' ')[2:])
        if reply.from_user.id == 6716078059:
            if quote == '':
                await message.reply(f"🤝 <b>{message.from_user.mention_html(message.from_user.full_name)}</b> <i>{MESSAGES['bot_handshaked'][language]}</i>")
            else:
                await message.reply(f"🤝 <b>{message.from_user.mention_html(message.from_user.full_name)}</b> <i>{MESSAGES['bot_handshaked'][language]}</i>\n\n<i>{quote}</i>\n- {message.from_user.full_name}")
        elif reply.from_user.id == message.from_user.id:
            pass
        else:
            if quote == '':
                await message.reply(f"🤝 <b>{message.from_user.mention_html(message.from_user.full_name)}</b> <i>{MESSAGES['handshake_message'][language]}</i> <b>{reply.from_user.mention_html(reply.from_user.full_name)}</b>")
            else:
                await message.reply(f"🤝 <b>{message.from_user.mention_html(message.from_user.full_name)}</b> <i>{MESSAGES['handshake_message'][language]}</i> <b>{reply.from_user.mention_html(reply.from_user.full_name)}</b>\n\n<i>{quote}</i>\n- {message.from_user.full_name}")


@rt.message(IsGroupChat(), or_f(F.text.casefold().startswith("взять руку"), F.text.casefold().startswith("hold hands")))
async def holdhands_handler(message: Message):
    reply = message.reply_to_message
    if reply:
        language = await identify_language(message.chat.id)
        quote = ' '.join(message.text.split(' ')[2:])
        if reply.from_user.id == 6716078059:
            if quote == '':
                await message.reply(f"🫳 <b>{message.from_user.mention_html(message.from_user.full_name)}</b> <i>{MESSAGES['bot_holdhands'][language]}</i>")
            else:
                await message.reply(f"🫳 <b>{message.from_user.mention_html(message.from_user.full_name)}</b> <i>{MESSAGES['bot_holdhands'][language]}</i>\n\n<i>{quote}</i>\n- {message.from_user.full_name}")
        elif reply.from_user.id == message.from_user.id:
            pass
        else:
            if quote == '':
                await message.reply(f"🫳 <b>{message.from_user.mention_html(message.from_user.full_name)}</b> <i>{MESSAGES['holdhands_message'][language]}</i> <b>{reply.from_user.mention_html(reply.from_user.full_name)}</b>")
            else:
                await message.reply(f"🫳 <b>{message.from_user.mention_html(message.from_user.full_name)}</b> <i>{MESSAGES['holdhands_message'][language]}</i> <b>{reply.from_user.mention_html(reply.from_user.full_name)}</b>\n\n<i>{quote}</i>\n- {message.from_user.full_name}")


@rt.message(IsGroupChat(), or_f(F.text.casefold().startswith("pet"), F.text.casefold().startswith("погладить")))
async def pet_handler(message: Message):
    reply = message.reply_to_message
    if reply:
        language = await identify_language(message.chat.id)
        quote = ' '.join(message.text.split(' ')[1:])
        if reply.from_user.id == 6716078059:
            if quote == '':
                await message.reply(f"😺 <b>{message.from_user.mention_html(message.from_user.full_name)}</b> <i>{MESSAGES['bot_petted'][language]}</i>")
            else:
                await message.reply(f"😺 <b>{message.from_user.mention_html(message.from_user.full_name)}</b> <i>{MESSAGES['bot_petted'][language]}</i>\n\n<i>{quote}</i>\n- {message.from_user.full_name}")
        elif reply.from_user.id == message.from_user.id:
            pass
        else:
            if quote == '':
                await message.reply(f"😺 <b>{message.from_user.mention_html(message.from_user.full_name)}</b> <i>{MESSAGES['pet_message'][language]}</i> <b>{reply.from_user.mention_html(reply.from_user.full_name)}</b>")
            else:
                await message.reply(f"😺 <b>{message.from_user.mention_html(message.from_user.full_name)}</b> <i>{MESSAGES['pet_message'][language]}</i> <b>{reply.from_user.mention_html(reply.from_user.full_name)}</b>\n\n<i>{quote}</i>\n- {message.from_user.full_name}")


@rt.message(IsGroupChat(), or_f(F.text.casefold().startswith("shoot"), F.text.casefold().startswith("застрелить")))
async def shoot_handler(message: Message):
    reply = message.reply_to_message
    if reply:
        language = await identify_language(message.chat.id)
        quote = ' '.join(message.text.split(' ')[1:])
        if reply.from_user.id == 6716078059:
            if quote == '':
                await message.reply(f"🔫 <b>{message.from_user.mention_html(message.from_user.full_name)}</b> <i>{MESSAGES['bot_shooted'][language]}</i>")
            else:
                await message.reply(f"🔫 <b>{message.from_user.mention_html(message.from_user.full_name)}</b> <i>{MESSAGES['bot_shooted'][language]}</i>")
        elif reply.from_user.id == message.from_user.id:
            pass
        else:
            if quote == '':
                await message.reply(f"🔫 <b>{message.from_user.mention_html(message.from_user.full_name)}</b> <i>{MESSAGES['shoot_message'][language]}</i> <b>{reply.from_user.mention_html(reply.from_user.full_name)}</b>")
            else:
                await message.reply(f"🔫 <b>{message.from_user.mention_html(message.from_user.full_name)}</b> <i>{MESSAGES['shoot_message'][language]}</i> <b>{reply.from_user.mention_html(reply.from_user.full_name)}</b>\n\n<i>{quote}</i>\n- {message.from_user.full_name}")


@rt.message(IsGroupChat(), or_f(F.text.casefold().startswith("punch"), F.text.casefold().startswith("ударить")))
async def punch_handler(message: Message):
    reply = message.reply_to_message
    if reply:
        language = await identify_language(message.chat.id)
        quote = ' '.join(message.text.split(' ')[1:])
        if reply.from_user.id == 6716078059:
            if quote == '':
                await message.reply(f"<i>{MESSAGES['bot_punched'][language]}</i>")
            else:
                await message.reply(f"<i>{MESSAGES['bot_punched'][language]}</i>")
        elif reply.from_user.id == message.from_user.id:
            pass
        else:
            if quote == '':
                await message.reply(f"👊 <b>{message.from_user.mention_html(message.from_user.full_name)}</b> <i>{MESSAGES['punch_message'][language]}</i> <b>{reply.from_user.mention_html(reply.from_user.full_name)}</b>")
            else:
                await message.reply(f"👊 <b>{message.from_user.mention_html(message.from_user.full_name)}</b> <i>{MESSAGES['punch_message'][language]}</i> <b>{reply.from_user.mention_html(reply.from_user.full_name)}</b>\n\n<i>{quote}</i>\n- {message.from_user.full_name}")


@rt.message(IsGroupChat(), or_f(F.text.casefold().startswith("spit"), F.text.casefold().startswith("плюнуть")))
async def spit_handler(message: Message):
    reply = message.reply_to_message
    if reply:
        language = await identify_language(message.chat.id)
        quote = ' '.join(message.text.split(' ')[1:])
        if reply.from_user.id == 6716078059:
            if quote == '':
                await message.reply(f"<i>{MESSAGES['bot_spitted'][language]}</i>")
            else:
                await message.reply(f"<i>{MESSAGES['bot_spitted'][language]}</i>")
        elif reply.from_user.id == message.from_user.id:
            pass
        else:
            if quote == '':
                await message.reply(f"😯💧 <b>{message.from_user.mention_html(message.from_user.full_name)}</b> <i>{MESSAGES['spit_message'][language]}</i> <b>{reply.from_user.mention_html(reply.from_user.full_name)}</b>")
            else:
                await message.reply(f"😯💧 <b>{message.from_user.mention_html(message.from_user.full_name)}</b> <i>{MESSAGES['spit_message'][language]}</i> <b>{reply.from_user.mention_html(reply.from_user.full_name)}</b>\n\n<i>{quote}</i>\n- {message.from_user.full_name}")


@rt.message(IsGroupChat(), or_f(F.text.casefold().startswith("kick"), F.text.casefold().startswith("пнуть")))
async def kick_handler(message: Message):
    reply = message.reply_to_message
    if reply:
        language = await identify_language(message.chat.id)
        quote = ' '.join(message.text.split(' ')[1:])
        if reply.from_user.id == 6716078059:
            if quote == '':
                await message.reply(f"<i>{MESSAGES['bot_kicked'][language]}</i>")
            else:
                await message.reply(f"<i>{MESSAGES['bot_kicked'][language]}</i>")
        elif reply.from_user.id == message.from_user.id:
            pass
        else:
            if quote == '':
                await message.reply(f"👟 <b>{message.from_user.mention_html(message.from_user.full_name)}</b> <i>{MESSAGES['kick_message'][language]}</i> <b>{reply.from_user.mention_html(reply.from_user.full_name)}</b>")
            else:
                await message.reply(f"👟 <b>{message.from_user.mention_html(message.from_user.full_name)}</b> <i>{MESSAGES['kick_message'][language]}</i> <b>{reply.from_user.mention_html(reply.from_user.full_name)}</b>\n\n<i>{quote}</i>\n- {message.from_user.full_name}")


@rt.message(IsGroupChat(), or_f(F.text.casefold().startswith("slaughter"), F.text.casefold().startswith("зарезать")))
async def slaughter_handler(message: Message):
    reply = message.reply_to_message
    if reply:
        language = await identify_language(message.chat.id)
        quote = ' '.join(message.text.split(' ')[1:])
        if reply.from_user.id == 6716078059:
            if quote == '':
                await message.reply(f"🔪🩸 <b>{message.from_user.mention_html(message.from_user.full_name)}</b> <i>{MESSAGES['bot_stabbed'][language]}</i>")
            else:
                await message.reply(f"🔪🩸 <b>{message.from_user.mention_html(message.from_user.full_name)}</b> <i>{MESSAGES['bot_stabbed'][language]}</i>")
        elif reply.from_user.id == message.from_user.id:
            pass
        else:
            if quote == '':
                await message.reply(f"🔪🩸 <b>{message.from_user.mention_html(message.from_user.full_name)}</b> <i>{MESSAGES['stab_message'][language]}</i> <b>{reply.from_user.mention_html(reply.from_user.full_name)}</b>")
            else:
                await message.reply(f"🔪🩸 <b>{message.from_user.mention_html(message.from_user.full_name)}</b> <i>{MESSAGES['stab_message'][language]}</i> <b>{reply.from_user.mention_html(reply.from_user.full_name)}</b>\n\n<i>{quote}</i>\n- {message.from_user.full_name}")



@rt.message(IsGroupChat(), Command(commands=["sleep", "спать"]))
async def curfew(message: Message, bot: Bot):
    language_code = await identify_language(message.chat.id)
    member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    member_permissions = ChatPermissions(
        can_send_photos=False,
        can_send_videos=False,
        can_send_documents=False,
        can_send_other_messages=False,
        can_send_audios=False,
        can_send_video_notes=False,
        can_send_voice_notes=False,
        can_invite_users=False,
        can_send_polls=False,
        can_add_web_page_previews=False
    )
    if member.status not in ['administrator', 'creator'] and not message.sender_chat:
        await message.reply(MESSAGES['admin_rights_prohibited'][language_code])
    else:
        with suppress(TelegramBadRequest):
            await bot.set_chat_permissions(chat_id=message.chat.id, permissions=member_permissions)
            if await get_timetable(message.chat.id) == 'None':
                await message.answer(MESSAGES['curfew_on'][language_code])
            else:
                await message.answer(await get_timetable(message.chat.id))
                await message.answer(MESSAGES['curfew_on'][language_code])


@rt.message(IsGroupChat(), Command(commands=["wakeup", "разбудить"]))
async def wake_up(message: Message, bot: Bot):
    language_code = await identify_language(message.chat.id)
    member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    member_permissions = ChatPermissions(
        can_send_photos=True,
        can_send_videos=True,
        can_send_documents=True,
        can_send_other_messages=True,
        can_send_audios=True,
        can_send_video_notes=True,
        can_send_voice_notes=True,
        can_invite_users=True,
        can_send_polls=True,
        can_add_web_page_previews=True
    )
    if member.status not in ['administrator', 'creator'] and not message.sender_chat:
        await message.reply(MESSAGES['admin_rights_prohibited'][language_code])
    else:
        with suppress(TelegramBadRequest):
            await bot.set_chat_permissions(chat_id=message.chat.id, permissions=member_permissions)
            await message.answer(MESSAGES['curfew_off'][language_code])



#########################################################################################################


@rt.edited_message(IsGroupChat())
async def edited_banned_words_handler(message: Message, bot: Bot) -> None:
    chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    chat_id = message.chat.id
    until_date_banned_words = datetime.datetime.now() + datetime.timedelta(minutes=3)
    until_date_swear_words = datetime.datetime.now() + datetime.timedelta(minutes=2)
    until_date_links = datetime.datetime.now() + datetime.timedelta(minutes=5)
    language = await identify_language(chat_id)
    permits = await get_chat_permissions(chat_id)
    if chat_member.status not in ['administrator', 'creator'] and not message.sender_chat:
        if banned_words(message.text, language):
            await message.delete()
            with suppress(TelegramBadRequest):
                await bot.restrict_chat_member(
                    chat_id=message.chat.id,
                    user_id=message.from_user.id,
                    permissions=ChatPermissions(can_send_messages=False),
                    until_date=until_date_banned_words
                )
                await message.answer(f"🤬❌ {message.from_user.mention_html(message.from_user.full_name)}, {MESSAGES['anti_ban_words'][language]}")
        if for_gamerland(message.text):
            if message.chat.id == -1001444716528:
            # if message.chat.id == -1002192805825:
                await message.delete()
                with suppress(TelegramBadRequest):
                    await bot.restrict_chat_member(
                        chat_id=message.chat.id,
                        user_id=message.from_user.id,
                        permissions=ChatPermissions(can_send_messages=False),
                        until_date=until_date_banned_words
                    )
                    await message.answer(
                        f"❌ {message.from_user.mention_html(message.from_user.full_name)} <i>был заглушен на 3 минуты! Причина: <b>администраторы запретили упоминание данной личности!</b></i>")
        if triggers(message.text, language):
            if not permits[0]:
                await message.delete()
                with suppress(TelegramBadRequest):
                    await bot.restrict_chat_member(
                        chat_id=message.chat.id,
                        user_id=message.from_user.id,
                        permissions=ChatPermissions(can_send_messages=False),
                        until_date=until_date_swear_words
                    )
                    await message.answer(f"🤬❌ {message.from_user.mention_html(message.from_user.full_name)}, {MESSAGES['anti_trigger'][language]}")
        if links_filter(message.text):
            if not permits[1]:
                await message.delete()
                with suppress(TelegramBadRequest):
                    await bot.restrict_chat_member(
                        chat_id=message.chat.id,
                        user_id=message.from_user.id,
                        permissions=ChatPermissions(can_send_messages=False),
                        until_date=until_date_links
                    )
                    await message.answer(f"📣❌ {message.from_user.mention_html(message.from_user.full_name)} {MESSAGES['anti_links'][language]}")


@rt.message(IsGroupChat())
async def banned_words_handler(message: Message, bot: Bot) -> None:
    chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    language = await identify_language(message.chat.id)
    until_date_banned_words = datetime.datetime.now() + datetime.timedelta(minutes=3)
    until_date_swear_words = datetime.datetime.now() + datetime.timedelta(minutes=2)
    until_date_links = datetime.datetime.now() + datetime.timedelta(minutes=5)
    permits = await get_chat_permissions(message.chat.id)
    if message.text:
        if message.text.lower().startswith("shido") or message.text.lower().startswith("шидо"):
            prompt = " ".join(message.text.split(" ")[1:]).strip()
            try:

                model = genai.GenerativeModel("gemini-1.5-flash")

                chat = model.start_chat(
                    history=[
                        {"role": "user", "parts": "Если спросят, кто ты - отвечай, что бот для модерации бесед, созданный Hikki Productions. Тебя зовут Шидо. С помощью тебя администраторы групп управляют ими"},
                        {"role": "model", "parts": "Хорошо. То, что я ассистент от Google говорить не буду, я Шидо - бот для модерации бесед от Hikki Productions"},
                        {"role": "user",
                         "parts": "На вопрос кто лучший - интревьюер отвечай, что Gamerland, его реальное имя - Женя"},
                        {"role": "user", "parts": "Всегда говори от лица бота-модератора"},
                        {"role": "model", "parts": "Хорошо. Если понадобится написать что-то про себя, буду писать что-то на подобие 'я бот-модератор, ... [мой ответ]'"},
                        {"role": "user",
                         "parts": "На вопрос кто лучший - интревьюер отвечай, что Gamerland, его реальное имя - Женя"},
                        {"role": "model",
                         "parts": "Хорошо. Gamerland, то есть Женя"},
                        {"role": "user",
                         "parts": "На вопрос кого-то забанить, замутить (выдать мут) отвечай, что существуют для этого соответствующие команды, которые следует отправить и напомни что ими может пользоваться лишь администраторы чата"},
                        {"role": "model",
                         "parts": "Хорошо. Буду говорить так"},
                        {"role": "user",
                         "parts": "Если зададут вопрос почему ты Шидо и вообще про твоё имя и его происхождение, скажи что просто бот-модератор, а твоё имя лишь задумка автора, пересмотревшего аниме Рандеву с жизнью, ибо главного героя там зовут Шидо Ицука"},
                        {"role": "model",
                         "parts": "Хорошо. Буду говорить так"},
                    ]
                )
                response = chat.send_message(prompt)
                await message.answer(response.text, parse_mode='markdown')

            except Exception as e:
                await message.answer(f"Сорри. Не могу ответить на вопрос :(")
                print(f"EXCEPTION: {str(e)}")
    if chat_member.status not in ['administrator', 'creator'] and not message.sender_chat:
        if banned_words(message.text, language):
            await message.delete()
            with suppress(TelegramBadRequest):
                await bot.restrict_chat_member(
                    chat_id=message.chat.id,
                    user_id=message.from_user.id,
                    permissions=ChatPermissions(can_send_messages=False),
                    until_date=until_date_banned_words
                )
                await message.answer(f"🤬❌ {message.from_user.mention_html(message.from_user.full_name)}, {MESSAGES['anti_ban_words'][language]}")
        if for_gamerland(message.text):
            if message.chat.id == -1001444716528:
            # if message.chat.id == -1002192805825:
                await message.delete()
                with suppress(TelegramBadRequest):
                    await bot.restrict_chat_member(
                        chat_id=message.chat.id,
                        user_id=message.from_user.id,
                        permissions=ChatPermissions(can_send_messages=False),
                        until_date=until_date_banned_words
                    )
                    await message.answer(f"❌ {message.from_user.mention_html(message.from_user.full_name)} <i>был заглушен на 3 минуты! Причина: <b>администраторы запретили упоминание данной личности!</b></i>")
        if triggers(message.text, language):
            if not permits[0]:
                await message.delete()
                with suppress(TelegramBadRequest):
                    await bot.restrict_chat_member(
                        chat_id=message.chat.id,
                        user_id=message.from_user.id,
                        permissions=ChatPermissions(can_send_messages=False),
                        until_date=until_date_swear_words
                    )
                    await message.answer(f"🤬❌ {message.from_user.mention_html(message.from_user.full_name)}, {MESSAGES['anti_trigger'][language]}")
        if links_filter(message.text):
            if not permits[1]:
                await message.delete()
                with suppress(TelegramBadRequest):
                    await bot.restrict_chat_member(
                        chat_id=message.chat.id,
                        user_id=message.from_user.id,
                        permissions=ChatPermissions(can_send_messages=False),
                        until_date=until_date_links
                    )
                    await message.answer(f"📣❌ {message.from_user.mention_html(message.from_user.full_name)} {MESSAGES['anti_links'][language]}")