from flask import Blueprint

main = Blueprint('app', __name__, url_prefix='/')

@main.route('/')
def index():
    return '<h1>Hello, World!</h1>'
