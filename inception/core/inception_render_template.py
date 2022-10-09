from flask import render_template
from inception.core.config import Page, PageConfig



def inception_render_template(template, config:PageConfig = PageConfig()):
    return render_template(template, current_page=Page(page_config=config))