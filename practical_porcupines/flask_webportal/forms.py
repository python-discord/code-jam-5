from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField

class DatePickerForm(FlaskForm):
    start_date = DateField(label="Start Date", id="startdate", format="%Y-%d-%m")
    end_date = DateField(label="End Date", id="enddate", format="%Y-%d-%m")
    submit  = SubmitField(label="Submit")