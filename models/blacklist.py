import uuid
from main import db, ma
from sqlalchemy.orm import Mapped, mapped_column


class Blacklist(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(db.String(120), nullable=False)
    app_uuid: Mapped[uuid.UUID] = mapped_column(db.String(36), nullable=False)
    blocked_reason: Mapped[str] = mapped_column(db.String(255), nullable=False)

    def __init__(self, email, app_uuid, blocked_reason):
        self.email = email
        self.app_uuid = app_uuid
        self.blocked_reason = blocked_reason

class BlacklistSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Blacklist
