from flask import Blueprint



bp_admin = Blueprint('admin', 'inception.admin', template_folder='templates', static_folder='static', static_url_path='/static/admin')
bp_auth = Blueprint('auth', 'inception.auth', template_folder='templates', static_folder='static', static_url_path='/static/auth')
bp_home = Blueprint('home', 'inception.home', template_folder='templates', static_folder='static', static_url_path='/static/home')
bp_api = Blueprint('jnatividad_api', 'inception.jnatividad')
