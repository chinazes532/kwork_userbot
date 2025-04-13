from src.database.models import async_session
from src.database.models import FirstMessage
from sqlalchemy import select


async def get_first_message(id):
    async with async_session() as session:
        msg = await session.scalar(select(FirstMessage).where(FirstMessage.id == id))
        return msg
