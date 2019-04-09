from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin

app = Flask(__name__)

app.config['SECRET_KEY'] = "123456790"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/npcj"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # added just to suppress a warning

db = SQLAlchemy(app)

# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


#app = Flask(__name__)
from app import views