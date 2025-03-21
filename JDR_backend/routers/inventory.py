from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import get_db, User, Inventory

inventory_router = APIRouter()

@inventory_router.get("/list", tags=["list"])
async def list_objects(username: str, db: Session = Depends(get_db)) -> list[dict]:
    """List all objects in a user's inventory"""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return {"error": "User not found"}
    
    inventory = db.query(Inventory).filter(Inventory.user_id == user.id).first()
    if not inventory:
        return {"error": "Inventory not found"}

    return inventory.get_items()
