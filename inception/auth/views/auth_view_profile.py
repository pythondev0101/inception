from inception.core.blueprints import bp_auth
from inception.core import inception_render_template



@bp_auth.route('/profile')
def profile():
    return inception_render_template('auth/profile_page.html')