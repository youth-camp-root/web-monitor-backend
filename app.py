from flask import Flask
from flasgger import Swagger
from flask_cors import CORS
from api.route.api import api
from api.mock.mock_data_forger import cmd
from flask_mongoengine import MongoEngine


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_pyfile('config.py')
    app.config['SWAGGER'] = {
        'title': 'Flask API Starter Kit',
    }

    Swagger(app)
    CORS(app, resources={r'/api/*': {'origins': '*'}})
    MongoEngine().init_app(app)

    app.register_blueprint(api)
    app.register_blueprint(cmd)

    return app


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5100,
                        type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app = create_app()

    app.run(host='0.0.0.0', port=port)
