from carpool import db

passengers = db.Table(
    "passengers",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("carpool_id", db.Integer, db.ForeignKey("carpool.id")),
)


class Carpool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True, unique=True)
    summary = db.Column(db.String(128))

    def __repr__(self):
        return "<Carpool: {}>".format(self.name)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True, unique=True)
    password = db.Column(db.String(32))
    carpools = db.relationship(
        "Carpool",
        secondary=passengers,
        primaryjoin=(passengers.c.user_id == id),
        secondaryjoin=(passengers.c.carpool_id == Carpool.id),
        backref=db.backref("passengers", lazy="dynamic"),
        lazy="dynamic",
    )

    def __repr__(self):
        return "<User: {}>".format(self.name)
