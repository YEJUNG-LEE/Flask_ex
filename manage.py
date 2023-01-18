from app import create_app, db
from flask_migrate import Migrate
from flask_script import Manager
from app.models import User

app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)