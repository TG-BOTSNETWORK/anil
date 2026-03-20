from sqlalchemy.orm import Session
from app.models.favorite import Favorite

def toggle_favorite(db: Session, user_id: int, news_id: int) -> bool:
    """
    Toggle a favorite for a user.
    Returns True if added, False if removed.
    """
    # Check if favorite already exists
    fav = db.query(Favorite).filter(
        Favorite.user_id == user_id,
        Favorite.news_item_id == news_id
    ).first()

    if fav:
        # Remove favorite
        db.delete(fav)
        db.commit()
        return False
    else:
        # Add favorite
        new_fav = Favorite(user_id=user_id, news_item_id=news_id)
        db.add(new_fav)
        db.commit()
        return True