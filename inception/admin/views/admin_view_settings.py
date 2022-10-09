from inception.core import inception_render_template
from inception.core.blueprints import bp_admin
from inception.core.config import PageConfig



@bp_admin.route('/settings')
def settings():
    page_config = PageConfig(sidebar_html='admin/sidebar_settings.html')

    return inception_render_template(
        'admin/settings_page.html',
        page_config
    )
