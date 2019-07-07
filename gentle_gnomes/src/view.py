import dataclasses
import logging

import quart
from quart import current_app as app
from quart import render_template

from .indicator import Indicator

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


@bp.route('/search/<city>/<indicator_name>')
async def search(city, indicator_name):
    async with app.app_context():
        indicator = Indicator(indicator_name, city)
        await indicator.populate_data()

    indicator_dict = indicator.to_dict()
    html = await render_template('view/indicator.html', indicator=indicator)
    indicator_dict.update({'html': html})

    response = {
        'indicator': indicator_dict,
        'nav_item': await render_template('view/nav_item.html', indicator=indicator),
    }

    return quart.jsonify(response)
