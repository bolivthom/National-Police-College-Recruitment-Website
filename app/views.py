"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app
from flask import render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin
from app.forms import LoginForm, SignUpForm
#from app.models import User
from werkzeug.security import check_password_hash



###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/login/')
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        if form.email.data:
            email = form.email.data
            password = form.password.data
            user = User.query.filter_by(email=email).first()
            if user is not None and check_password_hash(user.password, password):
                login_user(user)
                flash('Logged in successfully.', 'success')
                return redirect(url_for("dashboard"))
        else:
            flash('Username or Password is incorrect.', 'danger')
    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You were logged out', 'success')
    return redirect(url_for('home'))


@app.route('/sign-up/')
def signUp():
    form = SignUpForm()
    if request.method == "POST" and form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data
        confirm = form.confirm.data
        user = User.query.filter_by(email=email).first()
        if user is not None:
            db_session.add(User(first_name, last_name, email, password))
            db.session.commit()
            flash('Account created', 'success')
            return redirect(url_for("user"))
        else:
            flash('User with that email address already exist.', 'danger')
    """Render the website's login page."""
    return render_template('sign-up.html', form=form)


@app.route('/dashboard/<int:userid>')
@roles_required('Admin', 'Applicant')   
def dashboard():
    user = User.query.filter_by(id=userid).first()
    return render_template('dashboard.html', user=user)

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
