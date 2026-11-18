from datetime import datetime
from pydantic import BaseModel


class SlowResponse(BaseModel):
    message: str
    delay_seconds: int
    finished_at: datetime