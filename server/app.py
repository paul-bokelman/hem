import os
from flask import Flask
from globals import constants
from lib.load import preflight
from db.models import db, User, Action, Macro, MacroAction, UserAction
from services.routes.users import users_bp
from services.routes.macros import macros_bp
from services.routes.actions import actions_bp
from services.routes.pipelines import pipeline_bp
from flask_cors import CORS

preflight()

app = Flask(__name__)
CORS(app)
os.makedirs(constants.upload_folder, exist_ok=True)

# create the database tables if they don't exist
with db:
    db.create_tables([User, Action, Macro, MacroAction, UserAction])

# register route blueprints
app.register_blueprint(users_bp)
app.register_blueprint(macros_bp)
app.register_blueprint(actions_bp)
app.register_blueprint(pipeline_bp)

if __name__ == '__main__':
    app.run(port=8000, debug=True)
