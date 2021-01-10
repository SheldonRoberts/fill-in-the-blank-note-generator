from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.fields.html5 import IntegerRangeField
from flask_wtf.file import FileField

# note that the submit variables must have different names to be used on the same page

class AddNotes(FlaskForm):
    # form for handling simple text notes

    notes = TextAreaField()
    percent_blank = IntegerRangeField()
    submit1 = SubmitField('Generate Notes')

class AddDoc(FlaskForm):
    # form for handling .docx notes

    document = FileField()
    percent_blank = IntegerRangeField()
    submit2 = SubmitField('Generate Document')
