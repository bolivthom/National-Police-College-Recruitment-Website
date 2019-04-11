from . import db
from werkzeug.security import generate_password_hash
from flask_admin.contrib.sqla import ModelView

# User Model
class User(db.Model, UserMixin)):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.relationship('Role', secondary='user_role')

# Role Model
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

# Define the UserRoles association table
class UserRole(db.Model):
    __tablename__ = 'user_role'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))

# Applicant Model
class Applicant(db.Model): 
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))   
    mothers_maiden_name = db.Column(db.String(80))
    gender =  db.Column(db.String(80))
    #dob
    street1 =  db.Column(db.String(80))
    street2 =  db.Column(db.String(80))
    city =  db.Column(db.String(80))
    country =  db.Column(db.String(80))
    phone_number =  db.Column(db.String(80))
    trn =  db.Column(db.String(80))
    nis =  db.Column(db.String(80))
    brn =  db.Column(db.String(80))
    weight =  db.Column(db.String(80))
    height =  db.Column(db.String(80))
    place_of_birth =  db.Column(db.String(80))

    # Setup Flask-User and specify the User data-model
    user_manager = UserManager(app, db, User)


#Admin Model
#class Admin(db.Model):
#    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))

# Roles are defined by adding rows to the Role table with a specific Role.name value.
# admin_role = Role(name='Admin')
# applicant_role = Role(name='Applicant')
# db.session.commit()


def __init__(self, first_name, last_name, email, password, role):
     self.first_name = first_name
     self.last_name = last_name
     self.email = email
     self.password = generate_password_hash(password, method='pbkdf2:sha256'
     self.role = role)

     def is_authenticated(self):
         return True

     def is_active(self):
         return True

     def is_anonymous(self):
         return False

     def get_id(self):
         try:
             return unicode(self.id)  # python 2 support
         except NameError:
             return str(self.id)  # python 3 support

     def __repr__(self):
         return '<User %r>' % (self.email)

