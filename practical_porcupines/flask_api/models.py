from practical_porcupines.flask_api.app import db


class LevelModel(db.Model):
    """
    Contains mean values from each year & the corrosponding global water level
    """

    __tablename__ = "levels"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    wl = db.Column(db.Float)

    def __init__(self, date, wl):
        """
        > Gets date and water level
        - date: Datetime object
        - wl: Water level float of time
        """

        self.date = date
        self.wl = wl
