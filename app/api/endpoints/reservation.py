from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_reservation_intersections,
    get_meeting_room_or_404,
    get_reservation_or_404,
)
from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.reservation import reservation_crud
from app.models.user import User
from app.schemas.reservation import ReservationCreate, ReservationDB, ReservationUpdate

router = APIRouter()


@router.post(
    "/",
    response_model=ReservationDB,
)
async def create_reservation(
    reservation: ReservationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    await get_meeting_room_or_404(reservation.meetingroom_id, session)
    await check_reservation_intersections(**reservation.model_dump(), session=session)
    new_reservation = await reservation_crud.create(reservation, session, user)
    return new_reservation


@router.get(
    "/",
    response_model=list[ReservationDB],
)
async def get_all_reservations(
    session: AsyncSession = Depends(get_async_session),
):
    reservations = await reservation_crud.get_multi(session)

    return reservations


@router.delete(
    "/{reservation_id}",
    response_model=ReservationDB,
)
async def delete_reservation(
    reservation_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    reservation = await get_reservation_or_404(reservation_id, session)
    reservation = await reservation_crud.remove(reservation, session)

    return reservation


@router.patch(
    "/{reservation_id}",
    response_model=ReservationDB,
)
async def update_reservation(
    reservation_id: int,
    obj_in: ReservationUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    reservation = await get_reservation_or_404(reservation_id, session)
    await check_reservation_intersections(
        **obj_in.model_dump(),
        reservation_id=reservation_id,
        meetingroom_id=reservation.meetingroom_id,
        session=session,
    )
    reservation = await reservation_crud.update(reservation, obj_in, session)

    return reservation


@router.get(
    "/my_reservations",
    response_model=list[ReservationDB],
)
async def get_my_reservations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    reservations = await reservation_crud.get_by_user(
        user_id=user.id, session=session
    )

    return reservations
