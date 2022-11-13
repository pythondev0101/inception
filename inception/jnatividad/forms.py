from flask_wtf import FlaskForm
from app.admin.forms import AdminTableForm, AdminEditForm, AdminInlineForm, AdminField
from wtforms.validators import DataRequired
from wtforms import StringField



class SubscriberForm(AdminTableForm):
    from .models import SubArea

    __table_columns__ = ['First name','Last name',  'Sub Area','Created at', 'updated at']
    __heading__ = "Subscribers"

    fname = AdminField(label="First name",validators=[DataRequired()])
    lname = AdminField(label="Last name",validators=[DataRequired()])
    email = AdminField(label="Email Address",required=False)
    address = AdminField(label="Address",required=False)
    longitude = AdminField(label="Longitude", required=False)
    latitude = AdminField(label="Latitude", required=False)
    contract_number = AdminField(label="Contract No.", validators=[DataRequired()])
    sub_area_id = AdminField(label="Sub Area", model=SubArea, required=False)

    @property
    def fields(self):
        return [
            [self.fname,self.lname, self.contract_number],[self.email,self.address],[self.longitude,self.latitude],[self.sub_area_id]
            ]


class BillingForm(AdminTableForm):
    __table_columns__ = ['Status','Billing No.','Name', 'Description', 'Date From', 'Date To', 'Created By', 'Created At']
    __heading__ = 'Billings'

    number = AdminField(label='Billing No.',validators=[DataRequired()], readonly=True)
    name = AdminField(label="Name",validators=[DataRequired()])
    description = AdminField(label="Description",validators=[DataRequired()])
    date_from = AdminField(label="Date From", validators=[DataRequired()], type='date')
    date_to = AdminField(label="Date To", validators=[DataRequired()], type='date')

    @property
    def fields(self):
        return [[self.number ,self.name, self.description], [self.date_from, self.date_to]]


class BillingEditForm(AdminEditForm):
    __heading__ = 'Edit billing'

    number = AdminField(label='Billing No.',validators=[DataRequired()], readonly=True)
    name = AdminField(label="Name",validators=[DataRequired()])
    description = AdminField(label="Description",validators=[DataRequired()])
    date_from = AdminField(label="Date From", validators=[DataRequired()], type='date')
    date_to = AdminField(label="Date To", validators=[DataRequired()], type='date')

    @property
    def fields(self):
        return [[self.number ,self.name, self.description], [self.date_from, self.date_to]]


class DeliveriesInlineForm(AdminInlineForm):
    __table_id__ = 'tbl_inline_billings'
    __table_columns__ = ['Delivery id','Delivery Date','Date Delivered', 'Delivered By', 'Status', 'Actions']
    __title__ = "Billings"
    __html__ = 'bds/subscriber/deliveries_inline.html'


class SubscriberEditForm(AdminEditForm):
    from .models import SubArea

    __heading__ = 'Edit subscriber'

    fname = AdminField(label="First name",validators=[DataRequired()])
    lname = AdminField(label="Last name",validators=[DataRequired()])
    email = AdminField(label="Email Address",required=False)
    address = AdminField(label="Address",required=False)
    longitude = AdminField(label="Longitude", required=False)
    latitude = AdminField(label="Latitude", required=False)
    contract_number = AdminField(label="Contract No.", validators=[DataRequired()])
    sub_area_id = AdminField(label="Sub Area", required=False, model=SubArea)

    deliveries_inline = DeliveriesInlineForm()

    @property
    def fields(self):
        return [
            [self.fname,self.lname, self.contract_number],[self.email,self.address],[self.longitude,self.latitude],[self.sub_area_id]
            ]

    @property
    def inlines(self):
        return [self.deliveries_inline]


class MessengerForm(AdminTableForm):
    from .models import Area
    
    __table_columns__ = ['Username', 'First name', 'last name', 'email', 'created at', 'updated at']
    __heading__ = "Messengers"

    username = AdminField(label='Username', validators=[DataRequired()])
    email = AdminField(label='Email', type='email',required=False)
    fname = AdminField(label='First Name', validators=[DataRequired()])
    lname = AdminField(label='Last Name', validators=[DataRequired()])

    @property
    def fields(self):
        return [[self.fname, self.lname],[self.username,self.email]]


class MessengerAreasInline(AdminInlineForm):
    __table_id__ = 'tbl_inline_areas'
    __table_columns__ = ['Area name','Area Description','Municipality']
    __title__ = "Areas"
    __html__ = 'bds/messenger/bds_messenger_areas_inline.html'


class MessengerEditForm(AdminEditForm):
    from .models import Area

    __heading__ = 'Edit messenger'

    username = AdminField(label='Username', validators=[DataRequired()])
    email = AdminField(label='Email', type='email',required=False)
    fname = AdminField(label='First Name', validators=[DataRequired()])
    lname = AdminField(label='Last Name', validators=[DataRequired()])
    is_admin = AdminField(label='Is admin?',required=False, type='checkbox')

    areas_inline = MessengerAreasInline()

    @property
    def fields(self):
        return [[self.fname, self.lname],[self.username,self.email], [self.is_admin]]

    @property
    def inlines(self):
        return [self.areas_inline]


class SubAreaSubscriberInline(AdminInlineForm):
    __table_id__ = 'tbl_inline_subscribers'
    __table_columns__ = ['','Contract No.','first name','last name','Current Sub area']
    __title__ = "Subscribers"
    __html__ = None

    @property
    def buttons(self):
        _remove_button = """<button id="btn_delete_subscriber" type="button" 
                            class="mr-2 btn-icon btn-icon-only btn btn-outline-danger">
                            <i class="pe-7s-trash btn-icon-wrapper"> </i></button>
                        """
        _add_button = """<button type="button" class="btn-wide btn btn-success" data-toggle="modal" 
                            data-target="#add_subscriber_modal" data-placement="bottom">Add</button>
                            """
        return [
            _remove_button, _add_button
        ]


class SubAreaForm(AdminTableForm):
    from .models import Area

    __table_columns__ = ['Name', 'description', 'Created at', 'updated at']
    __heading__ = "Sub areas"

    name = AdminField(label="Name",validators=[DataRequired()])
    description = AdminField(label="Description", required=False)
    area_id = AdminField(label="Area", validators=[DataRequired()], model=Area)

    subscribers_inline = SubAreaSubscriberInline()

    @property
    def fields(self):
        return [
            [self.name, self.description],
            [self.area_id]
        ]

    @property
    def inlines(self):
        return [self.subscribers_inline]

class SubAreEditForm(AdminEditForm):
    from .models import Area

    __heading__ = "Sub areas"

    name = AdminField(label="Name",validators=[DataRequired()])
    description = AdminField(label="Description", required=False)
    area_id = AdminField(label="Area", validators=[DataRequired()], model=Area)

    subscribers_inline = SubAreaSubscriberInline()

    @property
    def fields(self):
        return [
            [self.name, self.description],
            [self.area_id]
        ]

    @property
    def inlines(self):
        return [self.subscribers_inline]


class AreaForm(AdminTableForm):
    from bds.models import Municipality

    __table_columns__ = ['Name', 'description', 'Municipality', 'Created at', 'updated at']
    __heading__ = "Areas"

    name = AdminField(label="Name",validators=[DataRequired()])
    description = AdminField(label="Description", required=False)
    municipality_id = AdminField(label="Municipality", required=False, model=Municipality)

    @property
    def fields(self):
        return [
            [self.name, self.description],
            [self.municipality_id]
        ]


class AreaEditForm(AdminEditForm):
    from bds.models import Municipality

    __heading__ = 'Edit Area'

    name = AdminField(label="Name",validators=[DataRequired()])
    description = AdminField(label="Description", required=False)
    municipality_id = AdminField(label="Municipality", required=False, model=Municipality)

    @property
    def fields(self):
        return []


class MunicipalityForm(AdminTableForm):
    __table_columns__ = ['Name', 'description', 'Created at', 'updated at']
    __heading__ = "Municipalities"

    name = AdminField(label="Name",validators=[DataRequired()])
    description = AdminField(label="Description", required=False)

    @property
    def fields(self):
        return [
            [self.name, self.description]
        ]


class MunicipalityEditForm(AdminEditForm):
    __heading__ = 'Edit municipality'

    name = AdminField(label="Name",validators=[DataRequired()])
    description = AdminField(label="Description", required=False)

    @property
    def fields(self):
        return [
            [self.name, self.description]
        ]

