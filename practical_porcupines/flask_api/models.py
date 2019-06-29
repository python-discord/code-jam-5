from practical_porcupines.flask_api.app import db

class LevelModel(db.Model):
    """
    Contains mean values from each year & the corrosponding global water level
    """

    __tablename__ = "levels"

    id = db.Column(db.Integer, primary_key=True)

    def __init__(self, id):
        self.id = id
    