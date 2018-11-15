from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from flask_wtf import CSRFProtect
import forms

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
csrf = CSRFProtect(app)

@app.route('/')                                  # Definición de ruta
def index():
    if 'logged_in' in session:
        message = "Notas de {}".format(session['username'])
    else:
        message = "Notas"
    
    return render_template('home.html', message = message)

@app.route('/notes')                             # Mostrar lectura de notas
def my_notes():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM notes WHERE user_id = %s", [session['user_id']])
    mysql.connection.commit()
    notes = cur.fetchall()
    cur.close()

    if result > 0:
        return render_template('notes.html', notes = notes)
    else:
        return render_template('notes.html')
        

    
@app.route('/note/<string:id>/')                 # Petición de una sola nota
def note(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM notes WHERE id = %s", (id))
    note = cur.fetchone()
    cur.close()
    return render_template('note.html', note = note)


@app.route('/add-note', methods = ['GET', 'POST'])
def add_note():
    form = forms.NoteForm(request.form)

    if request.method == 'POST' and form.validate():
        title = form.title.data
        description = form.description.data

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO notes(title, description, user_id) VALUES (%s, %s, %s)", (title, description, session['user_id']))
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

    form = forms.NoteForm(request.form)

    form.title.data = note['title']
    form.description.data = note['description']

    if request.method == 'POST' and form.validate:

        title = request.form['title']
        description = request.form['description']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE notes SET title = %s, description = %s WHERE id = %s", (title,description,id))
        mysql.connection.commit()
        cur.close()

        flash('Modificaste la nota exitosamente', 'success')

        return redirect(url_for('my_notes'))

    return render_template('edit_note.html', form = form)


@app.route('/delete-note/<string:id>', methods = ['POST'])
def delete_note(id):

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM notes WHERE id = %s", (id))
    mysql.connection.commit()
    cur.close()

    flash('Eliminaste la nota exitosamente', 'success')

    return redirect(url_for('my_notes'))


@app.route('/register', methods=['GET', 'POST'])
def register():
  form = forms.RegisterForm(request.form)
  if request.method == 'POST' and form.validate():
    name = form.name.data
    email = form.email.data
    username = form.username.data
    password = sha256_crypt.encrypt(str(form.password.data))
    
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))
    mysql.connection.commit()
    cur.close()

    flash('Estás registrado y puedes acceder', 'success')
    return redirect(url_for('index'))
  
  return render_template("login.html", form = form)

  
@app.route('/login', methods=['GET', 'POST'])
def login():
  form = forms.LoginForm(request.form)
  
  if request.method == 'POST' and form.validate():
    username = form.username.data
    password_candidate = form.password.data

    # Lógica
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", [username])
        result = cur.fetchone()
        print(result)
        cur.close()

        if sha256_crypt.verify(password_candidate, str(result['password'])):
            session['logged_in'] = True
            session['username'] = username
            session['user_id'] = result['id']

            return redirect(url_for('index'))
        else:
            flash('Usuario y/o Contraseña inválida', 'danger')

    except:
        flash('Usuario y/o Contraseña inválida', 'danger')

  return render_template("login.html", form = form)


@app.route('/logout')
def logout():
    session.clear()
    flash('Cerraste sesión exitosamente', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':      # Cuando el archivo sea el "main" entonces ejecuta la app
    app.secret_key = 'secret12345'
    app.run(debug=True) 

# Ataque CNF