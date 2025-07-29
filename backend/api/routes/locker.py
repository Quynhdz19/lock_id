from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from config.database import get_db, Locker, AccessLog, User
from api.routes.auth import get_current_active_user
from models.locker import LockerResponse, LockerListResponse, AccessLogResponse

router = APIRouter()

@router.get("/", response_model=LockerListResponse)
async def get_all_lockers(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all lockers"""
    lockers = db.query(Locker).all()
    
    locker_responses = []
    for locker in lockers:
        locker_responses.append(LockerResponse(
            id=locker.id,
            locker_number=locker.locker_number,
            is_occupied=locker.is_occupied,
            is_locked=locker.is_locked,
            current_user_id=locker.current_user_id,
            last_accessed=locker.last_accessed,
            created_at=locker.created_at,
            updated_at=locker.updated_at
        ))
    
    return LockerListResponse(lockers=locker_responses)

@router.get("/{locker_id}", response_model=LockerResponse)
async def get_locker(
    locker_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get specific locker by ID"""
    locker = db.query(Locker).filter(Locker.id == locker_id).first()
    
    if not locker:
        raise HTTPException(status_code=404, detail="Locker not found")
    
    return LockerResponse(
        id=locker.id,
        locker_number=locker.locker_number,
        is_occupied=locker.is_occupied,
        is_locked=locker.is_locked,
        current_user_id=locker.current_user_id,
        last_accessed=locker.last_accessed,
        created_at=locker.created_at,
        updated_at=locker.updated_at
    )

@router.post("/{locker_id}/unlock")
async def unlock_locker(
    locker_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Unlock a specific locker"""
    locker = db.query(Locker).filter(Locker.id == locker_id).first()
    
    if not locker:
        raise HTTPException(status_code=404, detail="Locker not found")
    
    if not locker.is_locked:
        raise HTTPException(status_code=400, detail="Locker is already unlocked")
    
    # Check if user has permission to unlock this locker
    if locker.current_user_id and locker.current_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You don't have permission to unlock this locker")
    
    # Unlock the locker
    locker.is_locked = False
    locker.last_accessed = datetime.utcnow()
    
    # Log the action
    access_log = AccessLog(
        user_id=current_user.id,
        locker_id=locker_id,
        action="unlock",
        success=True,
        timestamp=datetime.utcnow()
    )
    
    db.add(access_log)
    db.commit()
    
    return {"message": f"Locker {locker.locker_number} unlocked successfully"}

@router.post("/{locker_id}/lock")
async def lock_locker(
    locker_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Lock a specific locker"""
    locker = db.query(Locker).filter(Locker.id == locker_id).first()
    
    if not locker:
        raise HTTPException(status_code=404, detail="Locker not found")
    
    if locker.is_locked:
        raise HTTPException(status_code=400, detail="Locker is already locked")
    
    # Check if user has permission to lock this locker
    if locker.current_user_id and locker.current_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You don't have permission to lock this locker")
    
    # Lock the locker
    locker.is_locked = True
    locker.last_accessed = datetime.utcnow()
    
    # Log the action
    access_log = AccessLog(
        user_id=current_user.id,
        locker_id=locker_id,
        action="lock",
        success=True,
        timestamp=datetime.utcnow()
    )
    
    db.add(access_log)
    db.commit()
    
    return {"message": f"Locker {locker.locker_number} locked successfully"}

@router.post("/{locker_id}/occupy")
async def occupy_locker(
    locker_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Occupy a locker"""
    locker = db.query(Locker).filter(Locker.id == locker_id).first()
    
    if not locker:
        raise HTTPException(status_code=404, detail="Locker not found")
    
    if locker.is_occupied:
        raise HTTPException(status_code=400, detail="Locker is already occupied")
    
    # Occupy the locker
    locker.is_occupied = True
    locker.current_user_id = current_user.id
    locker.last_accessed = datetime.utcnow()
    
    # Log the action
    access_log = AccessLog(
        user_id=current_user.id,
        locker_id=locker_id,
        action="occupy",
        success=True,
        timestamp=datetime.utcnow()
    )
    
    db.add(access_log)
    db.commit()
    
    return {"message": f"Locker {locker.locker_number} occupied successfully"}

@router.post("/{locker_id}/release")
async def release_locker(
    locker_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Release a locker"""
    locker = db.query(Locker).filter(Locker.id == locker_id).first()
    
    if not locker:
        raise HTTPException(status_code=404, detail="Locker not found")
    
    if not locker.is_occupied:
        raise HTTPException(status_code=400, detail="Locker is not occupied")
    
    # Check if user has permission to release this locker
    if locker.current_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You don't have permission to release this locker")
    
    # Release the locker
    locker.is_occupied = False
    locker.current_user_id = None
    locker.is_locked = True  # Auto-lock when released
    locker.last_accessed = datetime.utcnow()
    
    # Log the action
    access_log = AccessLog(
        user_id=current_user.id,
        locker_id=locker_id,
        action="release",
        success=True,
        timestamp=datetime.utcnow()
    )
    
    db.add(access_log)
    db.commit()
    
    return {"message": f"Locker {locker.locker_number} released successfully"}

@router.get("/access-logs", response_model=List[AccessLogResponse])
async def get_access_logs(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get access logs for current user"""
    logs = db.query(AccessLog).filter(AccessLog.user_id == current_user.id).order_by(AccessLog.timestamp.desc()).limit(50).all()
    
    log_responses = []
    for log in logs:
        log_responses.append(AccessLogResponse(
            id=log.id,
            user_id=log.user_id,
            locker_id=log.locker_id,
            action=log.action,
            success=log.success,
            timestamp=log.timestamp,
            face_recognition_confidence=log.face_recognition_confidence
        ))
    
    return log_responses 