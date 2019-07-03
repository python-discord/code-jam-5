from carpool import app, db
from carpool.models import User, Carpool


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User, "Carpool": Carpool}
