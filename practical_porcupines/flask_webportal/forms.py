from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField

class DatePickerForm(FlaskForm):
    start_date = DateField(label="Start Date", id="startdate", format="%Y-%m-%d")
    end_date = DateField(label="End Date", id="enddate", format="%Y-%m-%d")
    submit  = SubmitField(label="Submit")

    def validate_on_submit(self):
        result = super(DatePickerForm, self).validate()
        if self.start_date.data == None or self.end_date.data == None:
            return False
        if self.start_date.data > self.end_date.data:
            return False
        else:
            return True