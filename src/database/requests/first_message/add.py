from src.database.models import async_session
from src.database.models import FirstMessage


async def set_first_message(message_id):
    async with async_session() as session:
        first_message = FirstMessage(message_id=message_id)
        session.add(first_message)
        await session.commit()