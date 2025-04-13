from src.database.models import async_session
from src.database.models import SecondMessage
from sqlalchemy import select


async def get_second_message(id):
    async with async_session() as session:
        msg = await session.scalar(select(SecondMessage).where(SecondMessage.id == id))
        return msg
