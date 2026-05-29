from database.db import db
from pgvector.sqlalchemy import Vector
from sqlalchemy import Text, ARRAY, Float


class Cafe(db.Model):
    __tablename__ = "cafes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(500), nullable=False)
    description = db.Column(Text, nullable=False)
    image = db.Column(db.String(300), nullable=False)
    tags = db.Column(db.String(500))           # comma-separated tags e.g. "cozy,espresso,wifi"
    hours = db.Column(db.String(200))
    price_range = db.Column(db.String(50))     # e.g. "₱80–₱250"

    # pgvector column — 1536 dims for OpenAI / 1024 for Anthropic embeddings
    # We'll use a simple 384-dim text embedding via a local approach,
    # but the column size can be adjusted. We'll store the embedding generated
    # from the cafe's description + tags.
    embedding = db.Column(Vector(384))

    # Relationship to menu items
    menu_items = db.relationship("MenuItem", backref="cafe", lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "description": self.description,
            "image": self.image,
            "tags": self.tags.split(",") if self.tags else [],
            "hours": self.hours,
            "price_range": self.price_range,
        }


class MenuItem(db.Model):
    __tablename__ = "menu_items"

    id = db.Column(db.Integer, primary_key=True)
    cafe_id = db.Column(db.Integer, db.ForeignKey("cafes.id"), nullable=False)
    category = db.Column(db.String(100), nullable=False)   # e.g. "Coffee", "Food", "Drinks"
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(Text)
    price = db.Column(db.String(50))                        # e.g. "₱120"

    def to_dict(self):
        return {
            "id": self.id,
            "category": self.category,
            "name": self.name,
            "description": self.description,
            "price": self.price,
        }
