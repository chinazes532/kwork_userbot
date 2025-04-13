from src.database.models import async_session
from src.database.models import SecondMessage


async def set_second_message(message_id):
    async with async_session() as session:
        second_message = SecondMessage(message_id=message_id)
        session.add(second_message)
        await session.commit()