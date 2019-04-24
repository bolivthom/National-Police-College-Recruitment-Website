"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app
from functools import wraps
from app import app, db, login_manager
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
from app.models import User, Role, SupportingDocs, Applicant
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from flask import render_template, request, redirect, url_for, flash, session
from app.forms import (
    LoginForm, SignUpForm, ApplicationForm, UploadSupportingDocs, UploadTrn,
    UploadNis, UploadNationalId, UploadBirthCertificate
)

"""
1. Is user logged out?
Yes - Show them only login or sign_up pages
No - Never show the above pages, redirect them to appropriate dashboard by default

I think is_authenticated or some method in the flask_login lob  help with this
could
2. Is user admin?
Yes - Enforce step 1 and that's it
No 
 - At this point, the user is definitely a particiapant
 - Prevent them from seeing any admin specific role

3. Is user participant?
Yes - Not much to do at this point, steps 1 & 2 take care of any pages they shouldn't see
No - N/A

"""


def is_admin(user):
    for role in user.roles:
        if role.name == 'Admin':
            return True
    return False


def is_applicant(user):
    for role in user.roles:
        if role.name == 'Applicant':
            return True
    return False


def get_user_dashboard_url(user):
    if is_admin(user):
        return url_for('admin_dashboard')
    return url_for('applicant_application')


def redirect_unauthorized_role(check_role):
    check_role_fallback_url_map = {
        is_admin: 'admin_dashboard',
        is_applicant: 'applicant_application',
    }

    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    if not check_role(current_user):
        route = check_role_fallback_url_map[check_role]
        url = url_for(route)
        return redirect(url)

    return None


def allow_applicant_role(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        unauthorized_redirect = redirect_unauthorized_role(is_applicant)
        if unauthorized_redirect:
            return unauthorized_redirect
        return f(*args, **kwargs)


def allow_admin_role(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        unauthorized_redirect = redirect_unauthorized_role(is_admin)
        if unauthorized_redirect:
            return unauthorized_redirect
        return f(*args, **kwargs)


def guest(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if current_user.is_authenticated:
            url = get_user_dashboard_url(current_user)
            return redirect(url)
        return f(*args, **kwargs)
    return decorator


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))

###
# Routing for your application.
###

@app.route('/')
@guest
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
@guest
def login():
    form = LoginForm(request.form)

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()

        is_credentials_valid = user and check_password_hash(user.password, password)

        if not is_credentials_valid:
            flash('Username or Password is incorrect.', 'danger')
        else:
            login_user(user)
            session['logged_in'] = True
            flash('Logged in successfully.', 'success')
            redirect_url = get_user_dashboard_url(user)
            return redirect(redirect_url)
    else:
        flash_errors(form)
    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    session['logged_in'] = False
    flash('You were logged out', 'success')
    return redirect(url_for('home'))


@app.route('/sign-up', methods=['GET', 'POST'])
@guest
def sign_up():
    form = SignUpForm(request.form)
    if form.validate_on_submit():
        email = form.email.data
        confirm = form.confirm.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        if user:
            flash('User with that email address already exist.', 'danger')
        else:
            user = User(email, password)
            applicant_role = Role.query.filter_by(name='Applicant').first()
            user.roles = [applicant_role,]

            db.session.add(user)
            db.session.commit()

            flash('Account created', 'success')

            login_url = url_for('login')
            return redirect(login_url)
    else:
        flash_errors(form)
    return render_template('sign-up.html', form=form)


@app.route('/application', methods=['GET', 'POST'])
@login_required
def applicant_application():
    applicant = Applicant.query.filter_by(user_id=current_user.id).first()
    if request.method == 'GET' and applicant:
        form = ApplicationForm(obj=applicant)
    else:
        form = ApplicationForm(request.form)

    upload_form = UploadSupportingDocs()
    upload_trn = UploadTrn()
    upload_nis = UploadNis()
    upload_national_id = UploadNationalId()
    upload_birth_certificate = UploadBirthCertificate()

    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        mothers_maiden_name = form.mothers_maiden_name.data
        gender = form.gender.data
        place_of_birth = form.place_of_birth.data
        phone_number = form.phone_number.data
        trn = form.trn.data
        nis = form.nis.data
        height = form.height.data
        weight = form.height.data
        street1 = form.street1.data
        street2 = form.street2.data
        city = form.city.data
        parish = form.parish.data
        country = form.country.data
        birth_certificateDoc = uploadForm.birth_certificate.data
        national_idDoc = uploadForm.national_id.data
        trnDoc = uploadForm.trn.data
        nisDoc = uploadForm.nis.data
        
        user = User.query.filter_by(id=current_user.id).first()

        if not user:
            flash('Error retreiving user', 'danger')
            return redirect(url_for('logout'))

        if not applicant:
            applicant = Applicant()
            applicant.user_id = user.id
            
            db.session.add(applicant)
            db.session.commit()

            print('new applicant:', applicant)    

        print('applicant:', applicant)

        applicant_updates = dict(
            first_name=first_name,
            last_name=last_name,
            mothers_maiden_name=mothers_maiden_name,
            place_of_birth=place_of_birth, 
            phone_number=phone_number,
            gender=gender, 
            height=height, 
            weight=weight,
            trn=trn, nis=nis,
            street1=street1,
            street2=street2,
            country=country,
            parish=parish,
            city=city,
        )

        Applicant.query.filter_by(user_id=user.id).update(applicant_updates)
        db.session.commit()

        # supportingDocs = SupportingDocs(userid=userid, national_id=national_idDoc, birth_certificate=birth_certificateDoc, trn=trnDoc, nis=nisDoc)
        
        # db.session.add(supportingDocs)
        # db.session.commit()
        
    return render_template(
        'applicant_application.html',
        form=form,
        upload_form=upload_form,
        upload_trn=upload_trn,
        upload_nis=upload_nis,
        upload_national_id=upload_national_id,
        upload_birth_certificate=upload_birth_certificate,
    )


@app.route('/applicant/dashboard')
@login_required
def applicant_dashboard():
    return render_template('applicant_dashboard.html')

@app.route('/applicant/application')
@login_required
def applicantApplication_view():
    return render_template('applicantApplication_View.html')

@app.route('/applicant/test-results')
@login_required
def applicantTestResults_view():
    return render_template('applicantTestResults_View.html')



@app.route('/admin')
@login_required  
def admin_dashboard():
    #user = User.query.filter_by(id=userid).first()
    #isAdmin = is_admin(user)
    #if isAdmin:
    return render_template('admin_dashboard.html')
    



# @app.route('/applicant/dashboard/<int:userid>')
#     @roles_required('Applicant')   
#     def applicant_page():
#         user = User.query.filter_by(id=userid).first()
#         return render_template('admin.html', user=user)


# @app.route('/user/<int:userid>')
# @login_required
# def user(userid, role):
#     user = User.query.filter_by(id=userid).first()
#     if user.role.name == 'Admin':
#         return render_template('admin.html', user=user)
#     elif user.role.name == 'Applicant':
#         return render_template('user.html', user=user)
#     return render_template('home.html')

# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
