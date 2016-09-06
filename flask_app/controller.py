from flask import render_template
from flask_app import fapp


@fapp.route('/<page>', defaults={'page': 'index'})
def main(page):
    return render_template('pages/%s.html' % page)
