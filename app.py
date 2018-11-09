from flask import Flask, render_template, request, redirect, url_for, flash
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

@app.route('/')                                  # Definición de ruta
def index():
    return render_template('home.html')

@app.route('/notes')                             # Mostrar lectura de notas
def my_notes():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM notes")
    mysql.connection.commit()
    notes = cur.fetchall()
    cur.close()

    if result > 0:
        return render_template('notes.html', notes = notes)
    else:
        return render_template('Sin datos')

    
@app.route('/note/<string:id>/')                 # Petición de una sola nota
def note(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM notes WHERE id = %s", (id))
    note = cur.fetchone()
    cur.close()
    return render_template('note.html', note = note)

class NoteForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=45)])
    description = TextAreaField('Description', [validators.Length(min=5)])

@app.route('/add-note', methods = ['GET', 'POST'])
def add_note():
    form = NoteForm(request.form)

    if request.method == 'POST' and form.validate():
        title = form.title.data
        description = form.description.data

        # Abrir la base
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO notes(title, description) VALUES (%s, %s)", (title, description))

        mysql.connection.commit()
        cur.close()

        flash('Agregaste la nota exitosamente', 'success')

        return redirect(url_for('add_note'))

    return render_template('add_note.html', form=form)


@app.route('/edit-note/<string:id>', methods = ['GET', 'POST'])
def edit_note(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM notes WHERE id = %s", (id))
    note = cur.fetchone()
    cur.close()

    form = NoteForm(request.form)

    form.title.data = note['title']
    form.description.data = note['description']

    if request.method == 'POST' and form.validate:

        title = request.form['title']
        description = request.form['description']

        # Abrir la base
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("UPDATE notes SET title = %s, description = %s WHERE id = %s", (title,description,id))

        mysql.connection.commit()
        cur.close()

        flash('Modificaste la nota exitosamente', 'success')

        return redirect(url_for('my_notes'))

    return render_template('edit_note.html', form = form)


@app.route('/delete-note/<string:id>', methods = ['POST'])
def delete_note(id):

    # Abrir la base
    cur = mysql.connection.cursor()

    # Execute query
    cur.execute("DELETE FROM notes WHERE id = %s", (id))

    # Commit DB
    mysql.connection.commit()
    
    # Cerrar la base
    cur.close()

    flash('Eliminaste la nota exitosamente', 'success')

    return redirect(url_for('my_notes'))


if __name__ == '__main__':      # Cuando el archivo sea el "main" entonces ejecuta la app
    app.secret_key = 'secret12345'
    app.run(debug=True) 

