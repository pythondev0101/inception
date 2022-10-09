from inception.core.blueprints import bp_admin
from inception.core import inception_render_template



@bp_admin.route('/dashboard')
def dashboard():
    return inception_render_template('admin/dashboard.html')
