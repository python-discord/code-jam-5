import json

from flask import Blueprint, current_app as app, render_template, request

from . import indicator

bp = Blueprint('view', __name__, url_prefix='/')


@bp.route('/')
def index():
    return render_template('view/index.html')


@bp.route('/search', methods=['POST'])
def search():
    try:
        location = json.loads(request.form['location'])
        latitude = location['lat']
        longitude = location['lng']
    except (json.JSONDecodeError, KeyError):
        return render_template('view/results.html')

    city = app.azavea.get_nearest_city(latitude, longitude)
    if city:
        with app.app_context():
            results = indicator.get_top_indicators(city)
    else:
        results = None

    return render_template('view/results.html', city=city, results=results)
