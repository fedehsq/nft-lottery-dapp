from flask import Flask, render_template, request
from nft_contract import w3
from views.home import home


def create_app(config="config.Development"):
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(home)
    return app

if __name__ == '__main__':
    from config import Development
    app = create_app(config=Development)
    app.run(debug=True)