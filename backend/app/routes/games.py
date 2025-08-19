# app/routes/games.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models import Game, Item
from app.schemas.games import GameRead
from app.schemas.items import ItemRead

router = APIRouter(prefix="/games", tags=["games"])

@router.get("/by-slug/{slug}", response_model=GameRead)
def get_game_by_slug(slug: str, db: Session = Depends(get_db)):


    game = db.query(Game).filter(Game.slug == slug).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game


@router.get("/", response_model=list[GameRead])
def list_games(db: Session = Depends(get_db)):
    return db.query(Game).all()

# @router.get("/by-slug/{slug}/items", response_model=list[ItemRead])
# def get_items_by_game(
#         slug: str,
#         q: str | None = Query(None, description="Search items by name"),
#         db: Session = Depends(get_db),
# ):
#         if slug == "all":
#             query = db.query(Item)
#         else:
#             game = db.query(Game).filter(Game.slug == slug).first()
#             if not game:
#                 raise HTTPException(status_code=404, detail="Game not found")
#             query = db.query(Item).filter(Item.game_id == game.id)
#
#         if q:
#             query = query.filter(Item.name.ilike(f"%{q}%"))
#
#         return query.all()
