from flask import flash, redirect, request, url_for
from flask_login import login_user
from werkzeug.urls import url_parse
from inception.core.blueprints import bp_auth
from inception.auth.models import User
from inception.core import inception_render_template



@bp_auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return inception_render_template('auth/auth_login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user: User = User.find_by_username(username)
        
        if not user:
            flash('Invalid username or password','error')
            return redirect(url_for('auth.login'))

        if user is None or not user.check_password(password):
            flash('Invalid username or password','error')
            return redirect(url_for('auth.login'))

        login_user(user, remember=False)
        
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('admin.dashboard')
        return redirect(next_page)
