import json

import quart
from quart import current_app as app
from quart import render_template

from . import indicator

bp = quart.Blueprint('view', __name__)


@bp.route('/')
async def index():
    return await render_template('view/index.html')


@bp.route('/search', methods=['POST'])
async def search():
    try:
        form = await quart.request.form
        location = json.loads(form['location'])
        latitude = location['lat']
        longitude = location['lng']
    except (json.JSONDecodeError, KeyError):
        return render_template('view/results.html')

    city = await app.azavea.get_nearest_city(latitude, longitude)
    if city:
        with app.app_context():
            results = await indicator.get_top_indicators(city)
    else:
        results = None

    return render_template('view/results.html', city=city, results=results)
