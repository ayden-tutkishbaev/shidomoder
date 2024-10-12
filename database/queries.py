from database.core import *

from sqlalchemy import text


async def add_data():
    async with async_session() as connect:
        query = """
        INSERT INTO bot_messages(how_to_add, commands_list, about_dev, addition_to_a_group, welcome_message, addition_photo)
        VALUES ('smth', 'smth', 'smth', 'smth', 'smth', 'smth')
        """
    await connect.execute(text(query))
    await connect.commit()


async def insert_id(chat_id, name_of_user):
    async with async_session() as connect:
        query = """
        INSERT INTO chats(chat_id, language_code, name_of_user)
        VALUES (:chat_id, 'eng', :name_of_user)
        """
        await connect.execute(text(query), {'chat_id': chat_id, 'name_of_user': name_of_user})
        await connect.commit()

async def insert_language(language, chat_id):
    async with async_session() as connect:
        query = """
        UPDATE chats
        SET language_code = :language_code
        WHERE chat_id = :chat_id
        """
        await connect.execute(text(query), {'language_code': language, 'chat_id': chat_id})
        await connect.commit()


async def identify_language(chat_id):
    async with async_session() as connect:
        query = """
        SELECT language_code FROM chats
        WHERE chat_id = :chat_id
        """
        data = await connect.execute(text(query), {'chat_id': chat_id})
        return data.fetchone()[0]


async def get_all_chats():
    async with async_session() as connect:
        data = await connect.execute(text("""
        SELECT chat_id FROM chats
        """))
        users = data.fetchall()
        chats = [user[0] for user in users]
        return chats


# def insert_eng_story(title, text):
#     database = sqlite3.connect("moder_bot.db")
#     cursor = database.cursor()
#     cursor.execute("""
#     INSERT INTO stories_eng(title, text)
#     VALUES (?, ?)
#     """, (title, text))
#     database.commit()
#     database.close()
#
#
# def insert_rus_story(title, text):
#     database = sqlite3.connect("moder_bot.db")
#     cursor = database.cursor()
#     cursor.execute("""
#     INSERT INTO stories_rus(title, text)
#     VALUES (?, ?)
#     """, (title, text))
#     database.commit()
#     database.close()


# def get_eng_story(random_id):
#     database = sqlite3.connect("moder_bot.db")
#     cursor = database.cursor()
#     cursor.execute("""
#     SELECT title, text FROM stories_eng
#     WHERE story_id = ?
#     """, (random_id,))
#     story = cursor.fetchone()
#     return story
#
#
# def get_eng_story_del(title):
#     database = sqlite3.connect("moder_bot.db")
#     cursor = database.cursor()
#     cursor.execute("""
#     SELECT title, text FROM stories_eng
#     WHERE title = ?
#     """, (title,))
#     story = cursor.fetchone()
#     return story
#
#
# def get_rus_story_del(title):
#     database = sqlite3.connect("moder_bot.db")
#     cursor = database.cursor()
#     cursor.execute("""
#     SELECT title, text FROM stories_rus
#     WHERE title = ?
#     """, (title,))
#     story = cursor.fetchone()
#     return story
#
#
# def get_all_eng_stories_ids():
#     database = sqlite3.connect("moder_bot.db")
#     cursor = database.cursor()
#     cursor.execute("""
#     SELECT story_id FROM stories_eng""")
#     story_ids = [story_id[0] for story_id in cursor.fetchall()]
#     return story_ids
#
#
# def get_all_rus_stories_ids():
#     database = sqlite3.connect("moder_bot.db")
#     cursor = database.cursor()
#     cursor.execute("""
#     SELECT story_id FROM stories_rus""")
#     story_ids = [story_id[0] for story_id in cursor.fetchall()]
#     return story_ids
#
#
# def get_rus_story(random_id):
#     database = sqlite3.connect("moder_bot.db")
#     cursor = database.cursor()
#     cursor.execute("""
#     SELECT title, text FROM stories_rus
#     WHERE story_id = ?
#     """, (random_id,))
#     story = cursor.fetchone()
#     return story
#
#
# def get_all_rus_stories_titles():
#     database = sqlite3.connect("moder_bot.db")
#     cursor = database.cursor()
#     cursor.execute("""
#     SELECT title FROM stories_rus""")
#     story_titles = [story_title[0] for story_title in cursor.fetchall()]
#     return story_titles
#
#
# def get_all_eng_stories_titles():
#     database = sqlite3.connect("moder_bot.db")
#     cursor = database.cursor()
#     cursor.execute("""
#     SELECT title FROM stories_eng""")
#     story_titles = [story_title[0] for story_title in cursor.fetchall()]
#     return story_titles
#
#
# def delete_eng_story(title):
#     database = sqlite3.connect("moder_bot.db")
#     cursor = database.cursor()
#     cursor.execute("""
#     DELETE FROM stories_eng WHERE title = ?
#     """, (title,))
#     database.commit()
#     database.close()
#
#
# def delete_rus_story(title):
#     database = sqlite3.connect("moder_bot.db")
#     cursor = database.cursor()
#     cursor.execute("""
#     DELETE FROM stories_rus WHERE title = ?
#     """, (title,))
#     database.commit()
#     database.close()


async def insert_id_to_chat_permissions(chat_id, group_title):
    async with async_session() as connect:
        query = """
        INSERT INTO groups(chat_id, is_swear_words, is_links, name_of_group, rules_message, off_table)
        VALUES (:chat_id, FALSE, TRUE, :group_title, '<i>Rules has not been set in this chat yet 🤷‍♂️</i>', 'None') ON CONFLICT DO NOTHING
        """
        await connect.execute(text(query), {'chat_id': chat_id, 'group_title': group_title})
        await connect.commit()


async def off_swears(chat_id):
    async with async_session() as connect:
        query = """
        UPDATE groups
        SET is_swear_words = False
        WHERE chat_id = :chat_id
        """
        await connect.execute(text(query), {'chat_id': chat_id})
        await connect.commit()


async def on_swears(chat_id):
    async with async_session() as connect:
        query = """
        UPDATE groups
        SET is_swear_words = True
        WHERE chat_id = :chat_id
        """
        await connect.execute(text(query), {'chat_id': chat_id})
        await connect.commit()


async def on_links(chat_id):
    async with async_session() as connect:
        query = """
        UPDATE groups
        SET is_links = True
        WHERE chat_id = :chat_id
        """
        await connect.execute(text(query), {'chat_id': chat_id})
        await connect.commit()


async def off_links(chat_id):
    async with async_session() as connect:
        query = """
        UPDATE groups
        SET is_links = False
        WHERE chat_id = :chat_id"""
        await connect.execute(text(query), {'chat_id': chat_id})
        await connect.commit()


async def get_chat_permissions(chat_id):
    async with async_session() as connect:
        query = """
        SELECT is_swear_words, is_links FROM groups
        WHERE chat_id = :chat_id
        """
        data = await connect.execute(text(query), {'chat_id': chat_id})
        return data.fetchone()


async def fill_all_rows(chat_id, is_swear_words, is_links):
    async with async_session() as connect:
        query = """
        INSERT INTO groups(chat_id, is_swear_words, is_links)
        VALUES (?, ?, ?)
        """
        await connect.execute(text(query), {'chat_id': chat_id, 'is_swear_words': is_swear_words, 'is_links': is_links})
        await connect.commit()

###################################################################

async def insert_all_members_to_chat(chat_id, chat_name, user_id, user_name):
    async with async_session() as connect:
        query = """
        INSERT INTO chat_and_karma(chat_id, chat_name, user_id, user_name, karma)
        VALUES (:chat_id, :chat_name, :user_id, :user_name, 0)
        """
        await connect.execute(text(query), {'chat_id': chat_id, 'chat_name': chat_name, 'user_id': user_id, 'user_name': user_name})
        await connect.commit()


async def check_users_karma(user_id, chat_id):
    async with async_session() as connect:
        query = """
        SELECT karma FROM chat_and_karma
        WHERE user_id = :user_id AND chat_id = :chat_id
        """
        data = await connect.execute(text(query), {'chat_id': chat_id, 'user_id': user_id})
        return data.fetchone()[0]


async def insert_new_karma(user_id, chat_id, karma):
    async with async_session() as connect:
        query = """
        UPDATE chat_and_karma
        SET karma = :karma
        WHERE chat_id = :chat_id AND user_id = :user_id
        """
        await connect.execute(text(query), {'chat_id': chat_id, 'user_id': user_id, 'karma': karma})
        await connect.commit()


async def get_chat_rules(chat_id):
    async with async_session() as connect:
        query = """
        SELECT rules_message FROM groups
        WHERE chat_id = :chat_id
        """
        data = await connect.execute(text(query), {'chat_id': chat_id})
        return data.fetchone()[0]


async def set_rules(rules, chat_id):
    async with async_session() as connect:
        query = """
        UPDATE groups
        SET rules_message = :rules
        WHERE chat_id = :chat_id
        """
        await connect.execute(text(query), {'rules': rules, 'chat_id': chat_id})
        await connect.commit()


async def set_welcome_message(message):
    async with async_session() as connect:
        query = """
        UPDATE bot_messages
        SET welcome_message = :message
        """
        await connect.execute(text(query), {'message': message})
        await connect.commit()


async def get_welcome_message():
    async with async_session() as connect:
        query = """
        SELECT welcome_message FROM bot_messages
        WHERE id = 1
        """
        data = await connect.execute(text(query))
        return data.fetchone()[0]


async def set_addition_to_a_group(message):
    async with async_session() as connect:
        query = """
        UPDATE bot_messages
        SET addition_to_a_group = :message
        """
        await connect.execute(text(query), {'message': message})
        await connect.commit()


async def get_addition_to_a_group():
    async with async_session() as connect:
        query = """
        SELECT addition_to_a_group FROM bot_messages
        WHERE id = 1
        """
        data = await connect.execute(text(query))
        return data.fetchone()[0]


async def set_commands_list(message):
    async with async_session() as connect:
        query = """
        UPDATE bot_messages
        SET commands_list = :message
        """
        await connect.execute(text(query), {'message': message})
        await connect.commit()


async def get_commands_list():
    async with async_session() as connect:
        query = """
        SELECT commands_list FROM bot_messages
        WHERE id = 1
        """
        data = await connect.execute(text(query))
        return data.fetchone()[0]


async def set_how_to_add(message):
    async with async_session() as connect:
        query = """
        UPDATE bot_messages
        SET how_to_add = :message
        """
        await connect.execute(text(query), {'message': message})
        await connect.commit()


async def get_how_to_add():
    async with async_session() as connect:
        query = """
        SELECT how_to_add FROM bot_messages
        WHERE id = 1
        """
        data = await connect.execute(text(query))
        return data.fetchone()[0]


async def set_about_dev(message):
    async with async_session() as connect:
        query = """
        UPDATE bot_messages
        SET about_dev = :message
        """
        await connect.execute(text(query), {'message': message})
        await connect.commit()


async def get_about_dev():
    async with async_session() as connect:
        query = """
        SELECT about_dev FROM bot_messages
        WHERE id = 1
        """
        data = await connect.execute(text(query))
        return data.fetchone()[0]


async def set_addition_photo(message):
    async with async_session() as connect:
        query = """
        UPDATE bot_messages
        SET addition_photo = :message
        """
        await connect.execute(text(query), {'message': message})
        await connect.commit()


async def get_addition_photo():
    async with async_session() as connect:
        query = """
        SELECT addition_photo FROM bot_messages
        WHERE id = 1
        """
        data = await connect.execute(text(query))
        return data.fetchone()[0]


async def set_timetable(off_table, chat_id):
    async with async_session() as connect:
        query = """
        UPDATE groups
        SET off_table = :off_table
        WHERE chat_id = :chat_id
        """
        await connect.execute(text(query), {'off_table': off_table, 'chat_id': chat_id})
        await connect.commit()


async def get_timetable(chat_id):
    async with async_session() as connect:
        query = """
        SELECT off_table FROM groups
        WHERE chat_id = :chat_id
        """
        data = await connect.execute(text(query), {'chat_id': chat_id})
        return data.fetchone()[0]