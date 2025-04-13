import os
from typing import Annotated
from dotenv import load_dotenv

from sqlalchemy import ForeignKey, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine


load_dotenv()


DB_URL = os.getenv("DB_URL")


engine = create_async_engine(url=DB_URL,
                             echo=True)

async_session = async_sessionmaker(engine)

intpk = Annotated[int, mapped_column(primary_key=True)]


class Base(AsyncAttrs, DeclarativeBase):
    pass


class FirstMessage(Base):
    __tablename__ = 'first_messages'

    id: Mapped[intpk]
    message_id: Mapped[int]


class SecondMessage(Base):
    __tablename__ = 'second_messages'

    id: Mapped[intpk]
    message_id: Mapped[int]


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)