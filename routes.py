from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
import os, random
from sqlalchemy import select
from decorators import admin_required
from datetime import datetime
from extensions import db, send_verification_email, send_reset_link
from models import User
from app import create_app
from werkzeug.security import check_password_hash, generate_password_hash
from tokens import generate_reset_token, verify_reset_token

app = create_app()

@app.route('/')
def index():
    return render_template('index.html', current_user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        if not User.exists(username) or not User.password_correct(username, password):
            error = "username or password is incorrect"
        else:
            #user = db.session.execute(db.select(User).where(User.name == username)).scalar()
            user = User.get_by_username(username)
            login_user(user)
            return redirect(url_for('index'))
        return render_template('account/login.html', error=error)
    else: # request method GET
        return render_template('account/login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        entered_password = request.form.get('password')
        password_confirmation = request.form.get('confirm_password')
        verification_code = f"{random.randint(0, 99999):05}"
        if entered_password != password_confirmation:
            error = 'Passwords do not match'
        elif User.exists(username):
            error = 'account with this username already exists'
        else:
            send_verification_email(verification_code, email)
            db.session.add(User(name=username, password=generate_password_hash(entered_password, method="pbkdf2:sha256", salt_length=8), is_admin=False, email=email, verification_code=verification_code, verified=False))
            db.session.commit()
        return render_template('account/register.html', error=error)
    else: # request method GET
        return render_template('account/register.html')

@login_required
@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        verification_code = str(request.form.get('verification_code'))
        if request.form.get("verification_code") == current_user.verification_code:
            current_user.verified = True
            db.session.commit()

            return render_template('index.html', current_user=current_user)
        error = "incorrect code"
        return redirect(url_for('account/verify.html', error=error))
    return render_template('verify.html')

@app.route('/forgot_password', methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get('email')
        user = User.get_by_email(email)
        if user:
            token = generate_reset_token(email)
            reset_url = url_for('reset_password', token=token, _external=True)
            send_reset_link(reset_url, email)
            print(reset_url)
        flash('If that account exists, instructions will be sent to your email')
    return render_template('account/forgot_password.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    email = verify_reset_token(token)
    if not email:
        flash("The link is invalid or expired", "danger")
        return redirect(url_for('forgot_password'))
    if request.method == "POST":
        new_password = request.form.get('password')
        user = User.get_by_email(email)

        user.password = generate_password_hash(new_password, method='pbkdf2:sha256', salt_length=8)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('reset_password.html', token=token)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")