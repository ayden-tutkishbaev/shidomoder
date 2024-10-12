from sqlalchemy import ForeignKey, BigInteger, String, Text, Boolean, UniqueConstraint
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import mapped_column, relationship, DeclarativeBase, Mapped

from dotenv import dotenv_values
import os

dotenv = dotenv_values(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

engine = create_async_engine(url=dotenv['DB_URL'], echo=True)

async_session = async_sessionmaker(engine)


class Base(DeclarativeBase, AsyncAttrs):
    ...


class BotMessages(Base):
    __tablename__ = 'bot_messages'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    how_to_add: Mapped[str] = mapped_column(Text, default="")
    commands_list: Mapped[str] = mapped_column(Text, default="")
    about_dev: Mapped[str] = mapped_column(Text, default="")
    addition_to_a_group: Mapped[str] = mapped_column(Text, default="")
    welcome_message: Mapped[str] = mapped_column(Text, default="")
    addition_photo: Mapped[str] = mapped_column(Text, default="")


class ChatPermissionsTable(Base):
    __tablename__ = 'groups'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id = mapped_column(BigInteger, unique=True)
    name_of_group: Mapped[str] = mapped_column(Text, default="")
    is_swear_words: Mapped[bool] = mapped_column(Boolean, default=False)
    is_links: Mapped[bool] = mapped_column(Boolean, default=True)
    rules_message: Mapped[str] = mapped_column(Text, default="")
    off_table: Mapped[str] = mapped_column(Text, default="")


class Languages(Base):
    __tablename__ = 'chats'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id = mapped_column(BigInteger, unique=True)
    name_of_user: Mapped[str] = mapped_column(Text, default="")
    language_code: Mapped[str] = mapped_column(String(20), default="", nullable=True)


class ChatAndKarma(Base):
    __tablename__ = 'chat_and_karma'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id = mapped_column(BigInteger)
    chat_name: Mapped[str] = mapped_column(Text, default="")
    user_id = mapped_column(BigInteger)
    user_name: Mapped[str] = mapped_column(Text, default="")
    karma: Mapped[int] = mapped_column(default=0, nullable=True)

    __table_args__ = (
        UniqueConstraint('chat_id', 'user_id', name='uix_chat_user'),
    )


async def async_main():
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.create_all)