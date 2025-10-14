from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "PENDING"
    STARTED = "STARTED"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    RETRY = "RETRY"
    REVOKED = "REVOKED"

class EmailRequest(BaseModel):
    to: EmailStr
    subject: str
    body: str
    from_email: Optional[str] = None

class TaskResponse(BaseModel):
    task_id: str
    status: str
    message: str

class TaskStatusResponse(BaseModel):
    task_id: str
    status: TaskStatus
    result: Optional[dict] = None
    error: Optional[str] = None
    progress: Optional[dict] = None