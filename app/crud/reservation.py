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
        from_reserve: datetime,
        to_reserve: datetime,
        meetingroom_id: int,
        session: AsyncSession,
    ):
        reservations = await session.execute(
            select(Reservation).where(
                Reservation.meetingroom_id == meetingroom_id,
                and_(
                    from_reserve <= Reservation.to_reserve,
                    to_reserve >= Reservation.from_reserve,
                ),
            )
        )
        reservations = reservations.scalars().all()

        return reservations


reservation_crud = CRUDReservation()
