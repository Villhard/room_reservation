from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.reservation import Reservation


class CRUDReservation(CRUDBase):
    def __init__(self):
        super().__init__(Reservation)

    async def get_reservations_at_the_same_time(
        self,
        from_reserve: datetime,
        to_reserve: datetime,
        session: AsyncSession,
    ):
        ...
        return []


reservation_crud = CRUDReservation()
