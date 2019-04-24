from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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

def create_role(name):
    role = models.Role.query.filter_by(name=name).first()
    if role:
        return role
    else:
        role = models.Role(name=name)

        db.session.add(role)
        db.session.commit()
        return role

def create_admin(email, password):
    admin_role = models.Role.query.filter_by(name='Admin').first()
    found = models.User.query.filter_by(email=email).first()

    if not found:
        user = models.User(email, password)
        user.roles = [admin_role,]

        db.session.add(user)
        db.session.commit()

try:
    create_role('Applicant')
    create_role('Admin')
    create_admin('admin@email.com', 'password')
except:
    print('unable to seed data')