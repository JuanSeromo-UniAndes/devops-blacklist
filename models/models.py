from main import ma, db


class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    app_uuid = db.Column(db.String(255))
    blocked_reason = db.Column(db.String(255))


class EmailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Email