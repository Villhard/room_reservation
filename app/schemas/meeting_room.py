from typing import Optional

from pydantic import BaseModel, Field, field_validator


class MeetingRoomBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None


class MeetingRoomCreate(MeetingRoomBase):
    name: str = Field(min_length=1, max_length=100)


class MeetingRoomUpdate(MeetingRoomBase):
    @field_validator("name")
    def name_cannot_be_null(cls, name):
        if name is None:
            raise ValueError("Имя переговорки не может быть пустым")
        return name


class MeetingRoomDB(MeetingRoomCreate):
    id: int

    class Config:
        orm_mode = True
