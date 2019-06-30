from flask_wtf import FlaskForm
from wtforms import DateField

class DatePickerForm(FlaskForm):
    start_date = DateField(label="Start Date")
    end_date = DateField(label="End Date")