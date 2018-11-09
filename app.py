from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators


app = Flask(__name__)           # Toma el nombre del archivo para inicializar en la clase
# notes = Notes()

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask_demo'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Init MySQL
mysql = MySQL(app)

@app.route('/')                 # Definición de ruta
def index():
    return render_template('home.html')

@app.route('/notes')                 # Definición de ruta
def my_notes():
    return render_template('notes.html')

#@app.route('/note/<string:id>/')                 # Definición de ruta
#def note(id):
#    for note in notes:
#        if note['id'] == int(id):
#            data = note
#            break
#    return render_template('note.html', note = data)

class NoteForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=45)])
    description = TextAreaField('Description', [validators.Length(min=5)])

@app.route('/add-note', methods = ['GET', 'POST'])
def add_note():
    form = NoteForm(request.form)

    if request.method == 'POST' and form.validate():
        title = form.title.data
        description = form.description.data

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute
        cur.execute("INSERT INTO notes(title, description) VALUES (%s, %s)", (title, description))

        mysql.connection.commit()

        cur.close()

        return redirect(url_for('add_note'))

    return render_template('add_note.html', form=form)


if __name__ == '__main__':      # Cuando el archivo sea el "main" entonces ejecuta la app
    app.run(debug=True) 

