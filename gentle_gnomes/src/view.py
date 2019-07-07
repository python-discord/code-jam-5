import dataclasses
import json
import logging

import quart
from quart import current_app as app
from quart import render_template

from . import indicator

log = logging.getLogger(__name__)

bp = quart.Blueprint('view', __name__)


@bp.route('/')
async def index():
    lat = quart.request.args.get('lat')
    lng = quart.request.args.get('lng')

    return await render_template('view/index.html', lat=lat, lng=lng)


@bp.route('/location')
async def location():
    try:
        latitude = str(quart.request.args['lat'])
        longitude = str(quart.request.args['lng'])
    except KeyError:
        log.info('Failed to get coordinates from parameters.')
        return quart.abort(400)

    city = await app.azavea.get_nearest_city(latitude, longitude)
    if not city:
        log.info(f'Could not find a city for {latitude}, {longitude}')
        return quart.abort(404)
    else:
        return quart.jsonify(dataclasses.asdict(city))


@bp.route('/search', methods=['POST'])
async def search():
    try:
        form = await quart.request.form
        location = json.loads(form['location'])
        latitude = str(location['lat'])
        longitude = str(location['lng'])
    except (json.JSONDecodeError, KeyError):
        return await render_template('view/results.html')

    city = await app.azavea.get_nearest_city(latitude, longitude)
    if city:
        async with app.app_context():
            results = await indicator.get_top_indicators(city)
    else:
        log.info(f'Could not find a city for {latitude}, {longitude}')
        results = None

    return await render_template('view/results.html', city=city, results=results)
