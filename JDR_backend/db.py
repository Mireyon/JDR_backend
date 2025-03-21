import json
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, event, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship

# SQLite Database URL
DATABASE_URL = "sqlite:///./test.db"

# Create Database Engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)  # One-to-one relationship
    items = Column(String, default="[]")  # Store as JSON string

    def get_items(self):
        """Retrieve items as a Python list"""
        return json.loads(self.items)

    def set_items(self, items_list):
        """Convert list to JSON string and store"""
        self.items = json.dumps(items_list)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, unique=True)
    is_admin = Column(Boolean, default=False)

    inventory = relationship("Inventory", backref="user", uselist=False)  # One-to-one relationship


@event.listens_for(User, "after_insert")
def create_inventory(mapper, connection, target):
    """Automatically create an inventory entry when a new user is created."""
    from sqlalchemy.orm import Session

    session = Session(bind=connection)
    inventory = Inventory(user_id=target.id, items=json.dumps([]))  # Ensure it's not None
    session.add(inventory)
    session.commit()

# Create the tables
Base.metadata.create_all(bind=engine)

def init_db():
    db = SessionLocal()
    if not db.query(User).filter_by(username="admin").first():
        user = User(username="admin", is_admin=True)
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"Initialized DB with user: {user.username}")
    db.close()

# Run initialization
init_db()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
