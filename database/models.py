"""
database/models.py — All database tables.

Tables:
  cafes          — cafe info + pgvector embedding
  menu_items     — items per cafe
  user_sessions  — anonymous browser sessions
  voice_logs     — every voice query made
  favorites      — saved cafes per session
"""

from database.db import db
from sqlalchemy import Text, DateTime, String, Integer, ForeignKey
from datetime import datetime, timezone

try:
    from pgvector.sqlalchemy import Vector
    PGVECTOR_AVAILABLE = True
except ImportError:
    PGVECTOR_AVAILABLE = False


class Cafe(db.Model):
    __tablename__ = "cafes"

    id          = db.Column(Integer, primary_key=True)
    name        = db.Column(String(200), nullable=False)
    address     = db.Column(String(500), nullable=False)
    description = db.Column(Text, nullable=False)
    image       = db.Column(String(300), nullable=False)
    tags        = db.Column(String(600))       # comma-separated, English + Filipino
    hours       = db.Column(String(200))
    price_range = db.Column(String(50))        # e.g. "₱100–₱250"

    if PGVECTOR_AVAILABLE:
        embedding = db.Column(Vector(384))

    menu_items = db.relationship(
        "MenuItem", backref="cafe", lazy=True, cascade="all, delete-orphan"
    )
    favorites = db.relationship(
        "Favorite", backref="cafe", lazy=True, cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id":          self.id,
            "name":        self.name,
            "address":     self.address,
            "description": self.description,
            "image":       self.image,
            "tags":        self.tags.split(",") if self.tags else [],
            "hours":       self.hours,
            "price_range": self.price_range,
        }


class MenuItem(db.Model):
    __tablename__ = "menu_items"

    id          = db.Column(Integer, primary_key=True)
    cafe_id     = db.Column(Integer, ForeignKey("cafes.id"), nullable=False)
    category    = db.Column(String(100), nullable=False)
    name        = db.Column(String(200), nullable=False)
    description = db.Column(Text)
    price       = db.Column(String(50))

    def to_dict(self):
        return {
            "id":          self.id,
            "category":    self.category,
            "name":        self.name,
            "description": self.description,
            "price":       self.price,
        }


class UserSession(db.Model):
    __tablename__ = "user_sessions"

    id            = db.Column(Integer, primary_key=True)
    session_token = db.Column(String(64), unique=True, nullable=False, index=True)
    created_at    = db.Column(DateTime, default=lambda: datetime.now(timezone.utc))
    last_seen     = db.Column(DateTime, default=lambda: datetime.now(timezone.utc))

    voice_logs = db.relationship(
        "VoiceLog", backref="session", lazy=True, cascade="all, delete-orphan"
    )
    favorites = db.relationship(
        "Favorite", backref="session", lazy=True, cascade="all, delete-orphan"
    )


class VoiceLog(db.Model):
    __tablename__ = "voice_logs"

    id              = db.Column(Integer, primary_key=True)
    session_id      = db.Column(Integer, ForeignKey("user_sessions.id"), nullable=True)
    query_text      = db.Column(Text, nullable=False)
    detected_lang   = db.Column(String(20), default="en")    # en / tl / taglish
    input_method    = db.Column(String(10), default="voice")  # voice / text
    recommended_ids = db.Column(Text)                         # JSON e.g. "[3,7]"
    created_at      = db.Column(DateTime, default=lambda: datetime.now(timezone.utc))


class Favorite(db.Model):
    __tablename__ = "favorites"

    id         = db.Column(Integer, primary_key=True)
    session_id = db.Column(Integer, ForeignKey("user_sessions.id"), nullable=False)
    cafe_id    = db.Column(Integer, ForeignKey("cafes.id"), nullable=False)
    saved_at   = db.Column(DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        db.UniqueConstraint("session_id", "cafe_id", name="uq_session_cafe"),
    )
