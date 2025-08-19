# app/routes/games.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models import Game
from app.schemas.games import GameRead

router = APIRouter(prefix="/games", tags=["games"])

@router.get("/by-slug/{slug}", response_model=GameRead)
def get_game_by_slug(slug: str, db: Session = Depends(get_db)):
    game = db.query(Game).filter(Game.slug == slug).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game
