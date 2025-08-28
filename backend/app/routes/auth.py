from datetime import timedelta, datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import SessionLocal
from app.models import User, BlacklistedToken
from app.schemas.users import UserCreate, UserLogin, Token, UserRead
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
    decode_access_token,
    security,   # 👈 теперь используем HTTPBearer
)
from app.core.settings import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/auth", tags=["auth"])


# -------------------
# Dependency для БД
# -------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------
# Регистрация
# -------------------
@router.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token(
        data={"sub": str(new_user.id)},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}


# -------------------
# Логин
# -------------------
@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": str(db_user.id)},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}


# -------------------
# Кто я
# -------------------
@router.get("/me", response_model=UserRead)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


# -------------------
# Логаут (блокируем токен)
# -------------------
@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    credentials = Depends(security),  # 👈 здесь раньше был oauth2_scheme
    db: Session = Depends(get_db),
):
    token = credentials.credentials  # 👈 теперь вытаскиваем строку токена
    try:
        payload = decode_access_token(token)
    except Exception:
        return  # Если токен невалиден, молча выходим

    jti = payload.get("jti")
    exp = payload.get("exp")
    sub = payload.get("sub")

    if not jti or not exp:
        return

    expires_at = datetime.fromtimestamp(int(exp), tz=timezone.utc)

    user_id = None
    if sub:
        try:
            user_id = int(sub)
        except (TypeError, ValueError):
            pass

    exists = db.query(BlacklistedToken).filter(BlacklistedToken.jti == jti).first()
    if not exists:
        db.add(BlacklistedToken(jti=jti, user_id=user_id, expires_at=expires_at))
        db.commit()
