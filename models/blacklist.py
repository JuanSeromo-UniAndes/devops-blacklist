import uuid
from datetime import datetime
from main import db, ma
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime


class Blacklist(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(db.String(120), nullable=False)
    app_uuid: Mapped[str] = mapped_column(db.String(36), nullable=False)
    blocked_reason: Mapped[str] = mapped_column(db.String(255), nullable=True)
    ip_address: Mapped[str] = mapped_column(db.String(45), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, email, app_uuid, blocked_reason, ip_address):
        self.email = email
        self.app_uuid = app_uuid
        self.blocked_reason = blocked_reason or "No reason provided"
        self.ip_address = ip_address
        self.created_at = datetime.utcnow()

class BlacklistSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Blacklist
