from pydantic import BaseModel
from typing import Optional

class FaceRegistration(BaseModel):
    user_id: int
    face_image_path: Optional[str] = None

class FaceVerification(BaseModel):
    user_id: int
    confidence: float

class FaceResponse(BaseModel):
    success: bool
    message: str
    user_id: Optional[int] = None
    face_image_path: Optional[str] = None
    confidence: Optional[float] = None
    locker_id: Optional[str] = None

class FaceDataResponse(BaseModel):
    user_id: int
    has_face_data: bool
    created_at: str

class AccessLogResponse(BaseModel):
    id: int
    user_id: Optional[int]
    locker_id: int
    action: str
    success: bool
    confidence: Optional[int]
    timestamp: str 