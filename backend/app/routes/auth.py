from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.database.session import SessionLocal
from app.models import User, BlacklistedToken
from app.schemas.users import UserCreate, UserLogin, Token, UserRead
from app.core.security import hash_password, verify_password, create_access_token, get_current_user
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.security import oauth2_scheme, decode_access_token

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
    # Проверяем, что пользователя с таким email нет
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Создаём нового пользователя
    new_user = User(
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Создаём токен с user_id в sub
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
    # Ищем пользователя по email
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Создаём токен с user_id в sub
    access_token = create_access_token(
        data={"sub": str(db_user.id)},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserRead)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    try:
        payload = decode_access_token(token)
    except Exception:
        # Если токен вообще невалиден — просто выходим без ошибки
        return

    jti = payload.get("jti")
    exp = payload.get("exp")
    sub = payload.get("sub")

    if not jti or not exp:
        return

    expires_at = datetime.fromtimestamp(int(exp), tz=timezone.utc)

    # user_id в BlacklistedToken можно хранить как None, если юзера уже нет
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
