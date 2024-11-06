from datetime import datetime, timedelta

from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict


FROM_TIME = (datetime.now() + timedelta(days=1)).isoformat(timespec="minutes")
TO_TIME = (datetime.now() + timedelta(days=1, hours=1)).isoformat(timespec="minutes")


class ReservationBase(BaseModel):
    from_reserve: datetime = Field(example=FROM_TIME)
    to_reserve: datetime = Field(example=TO_TIME)

    model_config = ConfigDict(extra="forbid")


class ReservationUpdate(ReservationBase):
    @field_validator("from_reserve")
    def check_from_reserve_later_than_now(cls, from_reserve):
        if from_reserve < datetime.now():
            raise ValueError(
                "Время начала бронирования должно быть позже текущего времени"
            )
        return from_reserve

    @model_validator(mode="after")
    def check_from_reserve_before_to_reserve(cls, reservation):
        if reservation.from_reserve > reservation.to_reserve:
            raise ValueError(
                "Время окончания бронирования должно быть позже времени начала бронирования"
            )
        return reservation


class ReservationCreate(ReservationUpdate):
    meetingroom_id: int = Field(gt=0)


class ReservationDB(ReservationBase):
    id: int
    meetingroom_id: int

    class Config:
        from_attributes = True
