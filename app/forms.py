from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, SelectField, HiddenField
from wtforms.validators import InputRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed

# Login Form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

#SignUpForm(FlaskForm)
class SignUpForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), validators.Length(min=6, max=35)])
    password = PasswordField('Password', validators=[InputRequired(), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    role = HiddenField('Role')

# Registration Form
class ApplicationForm(FlaskForm):
    mothers_maiden_name = StringField('First Name', validators=[InputRequired()])
    gender = SelectField('Gender', choices=[('Male', 'M'), ('Female', 'F')])
    #dob = StringField('First Name', validators=[InputRequired()])
    street1 = StringField('Street 1', validators=[InputRequired()])
    street2 = StringField('Street 2', validators=[InputRequired()])
    city = StringField('City', validators=[InputRequired()])
    country = StringField('Country', validators=[InputRequired()])
    phone_number = StringField('Phone Number', validators=[InputRequired()])
    trn = StringField('TRN', validators=[InputRequired()])
    nis = StringField('NIS', validators=[InputRequired()])
    brn = StringField('BRN', validators=[InputRequired()])
    weight = StringField('Weight', validators=[InputRequired()])
    height = StringField('Height', validators=[InputRequired()])
    place_of_birth = StringField('Place of Birth', validators=[InputRequired()])

# Supporting Docs
class UploadSupportingDocs(FlaskForm):
    birth_certificate = FileField('Upload Field', validators=[FileRequired(), FileAllowed(['txt', 'pdf', 'png', 'jpg', 'jpeg'])]) 
    passport = FileField('Upload Field', validators=[FileRequired(), FileAllowed(['txt', 'pdf', 'png', 'jpg', 'jpeg'])])
    national_id = FileField('Upload Field', validators=[FileRequired(), FileAllowed(['txt', 'pdf', 'png', 'jpg', 'jpeg'])])
    trn = FileField('Upload Field', validators=[FileRequired(), FileAllowed(['txt', 'pdf', 'png', 'jpg', 'jpeg'])])
    nis = FileField('Upload Field', validators=[FileRequired(), FileAllowed(['txt', 'pdf', 'png', 'jpg', 'jpeg'])])

# Applicant Tests
class UploadApplicantTest(FlaskForm):
    polygraph = SelectField('Status', choices=[('Pass', 'P'), ('Fail', 'F')])
    police_record = SelectField('Status', choices=[('Pass', 'P'), ('Fail', 'F')])
    physical = SelectField('Status', choices=[('Pass', 'P'), ('Fail', 'F')])
    written = SelectField('Status', choices=[('Pass', 'P'), ('Fail', 'F')])
