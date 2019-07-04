import json

from flask import Blueprint, current_app as app, flash, render_template, request

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
        flash('Location not found.')
        return render_template('view/index.html')

    city = app.azavea.get_nearest_city(latitude, longitude)
    if city:
        with app.app_context():
            results = indicator.get_top_indicators(city)
    else:
        flash('Location not found.')
        results = None

    return render_template('view/index.html', city=city, results=results)
