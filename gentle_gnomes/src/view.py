from flask import current_app as app, Blueprint, render_template, request, flash

from . import indicator

bp = Blueprint('view', __name__, url_prefix='/')


@bp.route('/')
def index():
    return render_template('view/index.html')


@bp.route('/search', methods=['POST'])
def search():
    location = request.form['location']

    city = app.azavea.get_city_id(location)
    if city:
        top = indicator.get_top_indicators(app.azavea, city)
        results = repr(top)
    else:
        flash('Location not found.')
        results = None

    return render_template('view/index.html', results=results)
