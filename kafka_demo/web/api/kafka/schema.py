from uuid import UUID

from pydantic import BaseModel


class TicketCreateSchema(BaseModel):
    title: str


class TicketSchema(TicketCreateSchema):
    id: UUID
    is_completed: bool = False

    class Config:
        orm_mode = True
