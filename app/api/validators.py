from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.meeting_room import meeting_room_crud
from app.crud.reservation import reservation_crud
from app.models.meeting_room import MeetingRoom
from app.models.reservation import Reservation


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


async def check_reservation_intersections(**kwargs):
    reservations = await reservation_crud.get_reservations_at_the_same_time(**kwargs)
    if reservations:
        raise HTTPException(
            status_code=422,
            detail=str(reservations),
        )


async def get_reservation_or_404(
    reservation_id: int,
    session: AsyncSession,
) -> Reservation:
    reservation = await reservation_crud.get(reservation_id, session)
    if reservation is None:
        raise HTTPException(
            status_code=404,
            detail="Бронь не найдена",
        )

    return reservation
