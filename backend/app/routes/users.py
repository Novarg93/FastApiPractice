from uuid import uuid4
from io import BytesIO
from pathlib import Path
from PIL import Image
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_user

from app.core.security import get_current_user, get_db, verify_password, hash_password
from app.core.settings import settings
from app.models.users import User
from app.schemas.users import PasswordChange, UserUpdate, UserRead

router = APIRouter(prefix="/users", tags=["users"])
ALLOWED = {"image/jpeg","image/png","image/webp"}
MAX_SIZE = 2*1024*1024

@router.post("/me/avatar", status_code=200)
async def upload_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if file.content_type not in ALLOWED:
        raise HTTPException(415, "Unsupported image type")
    data = await file.read()
    if len(data) > MAX_SIZE:
        raise HTTPException(413, "File too large")
    try:
        im = Image.open(BytesIO(data)).convert("RGB")
    except Exception:
        raise HTTPException(400, "Corrupted image")

    w,h = im.size; m=min(w,h)
    im = im.crop(((w-m)//2,(h-m)//2,(w+m)//2,(h+m)//2)).resize((256,256))

    user_dir = Path(settings.MEDIA_ROOT)/"avatars"/str(current_user.id)
    user_dir.mkdir(parents=True, exist_ok=True)
    fname = f"{uuid4().hex}.webp"
    fpath = user_dir/fname

    # удалить старый файл
    if current_user.avatar_url:
        try:
            rel = current_user.avatar_url.replace(settings.MEDIA_URL+"/","")
            old = Path(settings.MEDIA_ROOT)/rel
            if old.is_file(): old.unlink()
        except Exception: pass

    im.save(fpath, format="WEBP", quality=90)
    rel_url = f"{settings.MEDIA_URL}/avatars/{current_user.id}/{fname}"
    current_user.avatar_url = rel_url
    db.add(current_user); db.commit(); db.refresh(current_user)
    return {"avatar_url": rel_url}

@router.delete("/me/avatar", status_code=status.HTTP_204_NO_CONTENT)
def delete_avatar(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.avatar_url:
        try:
            rel = current_user.avatar_url.replace(settings.MEDIA_URL+"/","")
            p = Path(settings.MEDIA_ROOT)/rel
            if p.is_file(): p.unlink()
        except Exception: pass
        current_user.avatar_url = None
        db.add(current_user); db.commit()
    return


@router.post("/me/change_password", status_code=status.HTTP_204_NO_CONTENT)
def change_password(
    data: PasswordChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not verify_password(data.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect current password",
        )
    if data.new_password != data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password and confirmation do not match",
        )
    if len(data.new_password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be at least 8 characters",
        )
    current_user.hashed_password = hash_password(data.new_password)
    db.add(current_user)
    db.commit()
    return

@router.patch("/me", response_model=UserRead, status_code=status.HTTP_200_OK)
def change_name(
     data: UserUpdate,
     db: Session = Depends(get_db),
     current_user: User = Depends(get_current_user),
):
    new_name = (data.name or "").strip()

    if not new_name or current_user.name == new_name:
        return current_user

    current_user.name = new_name
    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    return current_user

@router.delete("/me")
def delete_user(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        )
    db.delete(user)
    db.commit()

    return {"User deleted"}