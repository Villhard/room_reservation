from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator


class ReservationBase(BaseModel):
    from_reserve: datetime
    to_reserve: datetime


class ReservationUpdate(ReservationBase):
    @field_validator("from_reserve")
    def check_from_reserve_later_than_now(cls, from_reserve):
        if from_reserve < datetime.now():
            raise ValueError(
                "Время начала бронирования должно быть позже текущего времени"
            )
        return from_reserve

    @model_validator(skip_on_field_errors=True)
    def check_from_reserve_before_to_reserve(cls, reservation):
        if reservation.from_reserve > reservation.to_reserve:
            raise ValueError(
                "Время окончания бронирования должно быть позже времени начала бронирования"
            )
        return reservation


class ReservationCreate(ReservationUpdate):
    meeting_room_id: int = Field(gt=0)


class ReservationDB(ReservationBase):
    id: int
    meeting_room_id: int

    class Config:
        orm_mode = True
