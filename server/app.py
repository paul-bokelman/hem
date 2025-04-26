from flask import Flask
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

def init_db():
    """Initialize the database and create tables if they don't exist."""
    with db:
        db.create_tables([User, Action, Macro, MacroAction, UserAction])

# register route blueprints
app.register_blueprint(users_bp)
app.register_blueprint(macros_bp)
app.register_blueprint(actions_bp)
app.register_blueprint(pipeline_bp)

if __name__ == '__main__':
    init_db()
    app.run(port=8000, debug=True)
