from io import BytesIO
from uuid import uuid4
from pathlib import Path

from PIL import Image
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from app.core.settings import settings
from app.core.security import get_current_user, get_db
from app.models.users import User

router = APIRouter(prefix="/users", tags=["users"])

MAX_SIZE = 2*1024*1024
ALLOWED = {"image/jpeg", "image/png", "image/webp"}

def _ensure_dir(p: Path): p.mkdir(parents=True, exist_ok=True)

@router.post("/me", status_code=200)
async def upload_avatar(
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    if file.content_type not in ALLOWED:
        raise HTTPException(415, "Unsupported Media Type")
    data = await file.read()
    if len(data) > MAX_SIZE:
        raise HTTPException(413, "Too large")

    try:
        im = Image.open(BytesIO(data)).convert("RGB")
    except Exception:
        raise HTTPException(415, "Unsupported Media Type")

    w, h = im.size
    m = min(w, h)
    left = (w - m) / 2
    top = (h - m) / 2
    im = im.crop((left, top, left+m, top+m)).resize((256, 256))

    user_dir = Path(settings.MEDIA_ROOT) / "avatars" / str(current_user.id)
    _ensure_dir(user_dir)
    fname = f"{uuid4().hex}.png"
    fpath = user_dir / fname

    if current_user.avatar_url:
        try:
            old = Path(settings.MEDIA_ROOT) / Path(current_user.avatar_url.replace(settings.MEDIA_URL+"/"))
            if old.is_file(): old.unlink()
        except Exception:
            pass

    im.save(fpath, format="WEBP", optimize=True, quality=90)

    rel_url = f"{settings.MEDIA_URL}/avatars/{current_user.id}/{fname}"
    current_user.avatar_url = rel_url
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return {"avatar_url": rel_url}


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_avatar(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    if current_user.avatar_url:
        try:
            p = Path(settings.MEDIA_ROOT) / Path(current_user.avatar_url.replace(settings.MEDIA_URL+"/"))
            if p.is_file(): p.unlink()
        except Exception:
            pass
        current_user.avatar_url = None
        db.add(current_user)
    return