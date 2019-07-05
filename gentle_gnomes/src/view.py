import json

from quart import abort, current_app as app, Blueprint, render_template, request, flash

from . import indicator

bp = Blueprint('view', __name__)


@bp.route('/')
async def index():
    return await render_template('view/index.html')


@bp.route('/search', methods=['POST'])
async def search():
    try:
        form = await request.form
        location = json.loads(form['location'])
        latitude = location['lat']
        longitude = location['lng']
    except (json.JSONDecodeError, KeyError):
        return abort(400)

    city = await app.azavea.get_nearest_city(latitude, longitude)
    if city:
        with app.app_context():
            top = await indicator.get_top_indicators(city)

        results = '\n'.join(f'{i.label}: {i.rate}' for i in top)
    else:
        await flash('Location not found.')
        results = None

    return await render_template('view/index.html', city=str(city), results=results)
