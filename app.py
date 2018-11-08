from flask import Flask, render_template
# from data import Notes
from flask_mysqldb import MySQL

app = Flask(__name__)           # Toma el nombre del archivo para inicializar en la clase
# notes = Notes()

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'spiderm4n'
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

if __name__ == '__main__':      # Cuando el archivo sea el "main" entonces ejecuta la app
    app.run(debug=True) 

