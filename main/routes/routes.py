from flask import Blueprint
from main.utils.logger import logger

main = Blueprint('app', __name__, url_prefix='/')

@main.route('/')
def index():
    logger.info("Hello, World!")
    return '<h1>Hello, World!</h1>'
