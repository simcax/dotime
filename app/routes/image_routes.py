'''Routes to serve static images'''

from flask import send_from_directory, Blueprint

bp1 = Blueprint('images_blueprint', __name__, url_prefix='/images')

@bp1.route("/hello.jpg")
def hello_jpg():
    '''Serve hello.jpg'''
    return send_from_directory('static/images','hello.jpg',mimetype='image/jpg')

@bp1.route("/oops.jpg")
def oops_jpg():
    '''Serve oops.jph'''
    return send_from_directory('static/images','oops.jpg',mimetype='image/jpg')
