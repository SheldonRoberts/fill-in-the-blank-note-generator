
import os
from flask import Flask, render_template, url_for, redirect, session, send_from_directory
from forms import AddNotes, AddDoc
from notegenerator import generate_notes, generate_docx
from werkzeug.utils import secure_filename

## TEMP
from docx import Document

# Initialize the Flask App
app = Flask(__name__)
# SECRET_KEY must be set to use session
app.config['SECRET_KEY'] = '\xa9\x81\xa3&\x87":$\xe9\xc6~P/#\x86\xf2\xf4A\xaaZ\x173/\xea'
app.config['UPLOAD_FOLDER'] = 'uploads'

filename = 'notes.docx'

# The index page will hold all the forms and information
@app.route('/', methods=['GET', 'POST'])
def index():

    # initialize the session variables to defaults
    if 'notes' not in session:
        session['notes'] = ""
    if 'blank-percent' not in session:
        session['blank-percent'] = 10

    # initialize the forms froms forms.py
    notes_form = AddNotes()
    docx_form = AddDoc()

    # set the notes to their previous value stored in session
    if not notes_form.notes.data:
        notes_form.notes.data = session['notes'] + ""

    # RAW Text Upload Form
    # form.validate_on_submit() doesn't work with multiple forms on one page,
    # this if statement must be used
    if notes_form.submit1.data and notes_form.validate():

        # notes: plain text to be given blanks
        # blank-percent: max ratio of words to be blanked out
        # variabled are stored in session to remain visable after refreshes
        session['notes'] = notes_form.notes.data
        session['blank-percent'] = notes_form.percent_blank.data
        return redirect(url_for('index'))

    # PDF Upload Form
    if docx_form.submit2.data and docx_form.validate():

        # the uploaded file is stores in the uploads directory
        docx_form.document.data.save(app.config['UPLOAD_FOLDER'] + '/' + filename)
        generate_docx(app.config['UPLOAD_FOLDER'] + '/' + filename, session['blank-percent'])
        return redirect(url_for('download'))

    # render the page, passing in the forms and notes
    return render_template('index.html', notes_form=notes_form, docx_form = docx_form,
                            notes=generate_notes(session['notes'], session['blank-percent']),
                            value=session['blank-percent'])

@app.route('/uploads/', methods=['GET', 'POST'])
def download():
    return send_from_directory(directory=app.config['UPLOAD_FOLDER'], filename=filename)

# run the app
if __name__ == '__main__':
    app.run(debug=True)
