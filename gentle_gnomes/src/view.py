from flask import Blueprint, render_template, request


bp = Blueprint('view', __name__, url_prefix='/')


@bp.route('/')
def index():
    return render_template('view/index.html')


@bp.route('/search', methods=['POST'])
def search():
    location = request.form['location']
    return render_template('view/results.html', results=location)
