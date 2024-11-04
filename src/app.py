import os
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from models import db
from dotenv import load_dotenv
from routes.characters import bp_character
from routes.users import bp_user
from routes.planets import bp_planet
from routes.favorites import bp_favorite

load_dotenv()

PATH = os.path.abspath('instance')

app = Flask(__name__, instance_path=PATH)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')

db.init_app(app)

Migrate(app, db)
CORS(app)

app.register_blueprint(bp_character)
app.register_blueprint(bp_user)
app.register_blueprint(bp_planet)
app.register_blueprint(bp_favorite)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)