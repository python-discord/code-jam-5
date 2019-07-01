import requests
from flask import current_app as app, Blueprint, render_template, request

BASE_URL = 'https://app.climate.azavea.com'

bp = Blueprint('view', __name__, url_prefix='/')


@bp.route('/')
def index():
    return render_template('view/index.html')


@bp.route('/search', methods=['POST'])
def search():
    location = request.form['location']
    headers = {'Authorization': f'Token {app.config["AZAVEA_TOKEN"]}'}

    cities = requests.get(f'{BASE_URL}/api/city', headers=headers, params={'name': location})
    cities.raise_for_status()

    cities = cities.json()
    if cities['count'] < 1:
        return render_template('view/results.html', results='City not found.')

    city_id = cities['features'][0]['id']

    hwi_url = f'{BASE_URL}/api/climate-data/{city_id}/RCP85/indicator/total_precipitation/'
    hwi = requests.get(hwi_url, headers=headers)
    hwi.raise_for_status()

    hwi = hwi.json()['data']

    return render_template('view/results.html', results=repr(hwi))
