from datetime import datetime
from pydantic import BaseModel


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""

        from_attributes = True


class NotificationBase(TunedModel):
    notification_id: int
    user_id: int
    timestamp: datetime
    status: bool
    text: str


class NotificationResponse(NotificationBase):
    pass
