from practical_porcupines.flask_api.app import db


class LevelModel(db.Model):
    """
    Contains mean values from each year & the corrosponding global water level
    """

    __tablename__ = "levels"

    date_id = db.Column(db.DateTime, primary_key=True)
    wl = db.Column(db.Float)

    def __init__(self, date_id, wl):
        """
        > Gets date and water level
        - date_id: Datetime object
        - wl: Water level float of time
        """

        self.date_id = date_id
        self.wl = wl
