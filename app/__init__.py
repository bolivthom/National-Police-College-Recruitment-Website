from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = "12345679123456789"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root@localhost:3308/npcj"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # added just to suppress a warning

# Flask-User settings
app.config['USER_APP_NAME'] = "Flask-User QuickStart App"      # Shown in and email templates and page footers
app.config['USER_ENABLE_EMAIL'] = False      # Disable email authentication
app.config['USER_ENABLE_USERNAME'] = True    # Enable username authentication
app.config['USER_REQUIRE_RETYPE_PASSWORD'] = False    # Simplify register form

db = SQLAlchemy(app)

# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#app = Flask(__name__)
from app import views
from app import models

