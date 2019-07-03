import json

from flask import abort, current_app as app, Blueprint, render_template, request, flash

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
        return abort(400)

    city = app.azavea.get_nearest_city(latitude, longitude)
    if city:
        top = indicator.get_top_indicators(city, app.azavea)
        results = '\n'.join(f'{i.label}: {i.rate}' for i in top)
    else:
        flash('Location not found.')
        results = None

    return render_template('view/index.html', city=str(city), results=results)
