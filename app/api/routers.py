from fastapi import APIRouter

from app.api.endpoints import meeting_room_router, reservation_router

main_router = APIRouter()
main_router.include_router(meeting_room_router)
main_router.include_router(reservation_router)
