from telethon import TelegramClient

client = TelegramClient('session_name', 26059888, "2f7d3e14e3f0ff8f86c7b402cd5e5f75",)


async def get_chat_members(chat_id):
    await client.start(bot_token='6716078059:AAHkjoM9qO-99g2UGAzceEZIx8gbUvMtUpo')
    members: list[dict] = []
    async for member in client.iter_participants(chat_id):
        members.append(
            {
                'user_id': member.id,
                'first_name': member.first_name,
            }
        )
    await client.disconnect()
    return members

