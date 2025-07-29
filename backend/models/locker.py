from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class LockerResponse(BaseModel):
    id: int
    locker_number: str
    is_occupied: bool
    is_locked: bool
    current_user_id: Optional[int] = None
    last_accessed: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class LockerListResponse(BaseModel):
    lockers: List[LockerResponse]

class AccessLogResponse(BaseModel):
    id: int
    user_id: int
    locker_id: int
    action: str
    success: bool
    timestamp: datetime
    face_recognition_confidence: Optional[int] = None
    
    class Config:
        from_attributes = True

class LockerStatus(BaseModel):
    total_lockers: int
    occupied_lockers: int
    available_lockers: int
    locked_lockers: int
    unlocked_lockers: int
    utilization_rate: float

class LockerAction(BaseModel):
    action: str  # "lock", "unlock", "assign", "release"
    user_id: Optional[int] = None 