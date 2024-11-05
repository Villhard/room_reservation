from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.meeting_room import meeting_room_crud
from app.models.meeting_room import MeetingRoom


async def check_name_dublicate(
    name: str,
    session: AsyncSession,
) -> None:
    room_id = await meeting_room_crud.get_room_id_by_name(name, session)
    if room_id is not None:
        raise HTTPException(
            status_code=422,
            detail="Переговорка с таким именем уже существует",
        )


async def get_meeting_room_or_404(
    meeting_room_id: int,
    session: AsyncSession,
) -> MeetingRoom:
    meeting_room = await meeting_room_crud.get(meeting_room_id, session)
    if meeting_room is None:
        raise HTTPException(
            status_code=404,
            detail="Переговорка не найдена",
        )

    return meeting_room
