from inception.core.blueprints import bp_admin
from inception.core import inception_render_template



@bp_admin.route('/users')
def users():
    return inception_render_template('admin/users.html')
