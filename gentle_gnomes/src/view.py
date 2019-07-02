from flask import current_app as app, Blueprint, render_template, request

from . import data

bp = Blueprint('view', __name__, url_prefix='/')


@bp.route('/')
def index():
    return render_template('view/index.html')


@bp.route('/search', methods=['POST'])
def search():
    location = request.form['location']

    city = app.azavea.get_city_id(location)
    if not city:
        return render_template('view/results.html', results='City not found.')

    top = data.get_top_indicators(app.azavea, city)

    return render_template('view/results.html', results=repr(top))
