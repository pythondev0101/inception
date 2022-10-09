from flask import redirect, url_for
from flask_login import current_user
from inception.core.blueprints import bp_home



@bp_home.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    else:
        return redirect(url_for('auth.login'))
    