from bson import ObjectId
from flask_weasyprint import HTML, render_pdf
from flask import render_template
from inception import MONGO
from inception.core.blueprints import bp_admin
from inception.core import inception_render_template
from inception.jnatividad.models import Municipality, SubArea, Billing, Delivery, Area



@bp_admin.route('/reports')
def reports():
    billings = Billing.find_all()
    municipalities = Municipality.find_all()
    
    return inception_render_template('admin/jnatividad_reports_page.html', billings=billings, municipalities=municipalities)


@bp_admin.route('/delivery-summary-per-sub-area-report.pdf')
def delivery_summary_per_sub_area_report():
    sub_area = ""
    area = ""
    municipality = ""
    billing = ""
    
    html = render_template(
        'admin/delivery_summary_per_sub_area_report.html', 
        deliveries=[],
        sub_area=sub_area,
        area=area,
        municipality=municipality,
        billing=billing
    )
    return render_pdf(HTML(string=html))