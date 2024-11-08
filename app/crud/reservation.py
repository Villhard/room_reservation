from typing import Optional
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.crud.base import CRUDBase
from app.models.reservation import Reservation


class CRUDReservation(CRUDBase):
    def __init__(self):
        super().__init__(Reservation)

    async def get_reservations_at_the_same_time(
        self,
        *,
        from_reserve: datetime,
        to_reserve: datetime,
        meetingroom_id: int,
        reservation_id: Optional[int] = None,
        session: AsyncSession,
    ):
        select_stmt = select(Reservation).where(
            Reservation.meetingroom_id == meetingroom_id,
            and_(
                from_reserve <= Reservation.to_reserve,
                to_reserve >= Reservation.from_reserve,
            ),
        )

        if reservation_id is not None:
            select_stmt = select_stmt.where(Reservation.id != reservation_id)

        reservations = await session.execute(select_stmt)

        return reservations.scalars().all()

    async def get_future_reservations_for_room(
        self,
        room_id: int,
        session: AsyncSession,
    ):
        reservations = await session.execute(
            select(Reservation).where(
                Reservation.meetingroom_id == room_id,
                Reservation.to_reserve > datetime.now(),
            )
        )

        return reservations.scalars().all()

    async def get_by_user(
        self,
        user_id: int,
        session: AsyncSession,
    ):
        reservations = await session.execute(
            select(Reservation).where(Reservation.user_id == user_id)
        )

        return reservations.scalars().all()


reservation_crud = CRUDReservation()
