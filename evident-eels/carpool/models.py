from carpool import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from carpool import login_manager

passengers = db.Table(
    "passengers",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("carpool_id", db.Integer, db.ForeignKey("carpool.id")),
)


class Carpool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True, unique=True)
    summary = db.Column(db.String(128))
    time_created = db.Column(db.DateTime(), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    from_location = db.Column(db.String(32))
    to_location = db.Column(db.String(32))

    @staticmethod
    def get_all():
        return Carpool.query.order_by(db.desc(Carpool.time_created))

    def __repr__(self):
        return "<Carpool: {}>".format(self.name)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True, unique=True)
    password = db.Column(
        db.String(200), primary_key=False, unique=False, nullable=False
    )
    email = db.Column(db.String(40), index=True, unique=True, nullable=False)
    carpools = db.relationship(
        "Carpool",
        secondary=passengers,
        primaryjoin=(passengers.c.user_id == id),
        secondaryjoin=(passengers.c.carpool_id == Carpool.id),
        backref=db.backref("passengers", lazy="dynamic"),
        lazy="dynamic",
    )
    created_carpools = db.relationship("Carpool", backref="creator")

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method="sha256")

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return "<User: {}>".format(self.name)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
