from flask import render_template
from flask_app import fapp


@fapp.route('/<page>', defaults={'page': 'index'})
def main(page):
    return render_template('pages/{0!s}.html'.format(page))
