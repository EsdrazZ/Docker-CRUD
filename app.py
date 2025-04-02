from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import time
from sqlalchemy.exc import OperationalError

app = Flask(__name__)

# Configuración de la base de datos
DATABASE_USER = os.getenv('POSTGRES_USER', 'root')
DATABASE_PASSWORD = os.getenv('POSTGRES_PASSWORD', '123456789')
DATABASE_NAME = os.getenv('POSTGRES_DB', 'crud_test')
DATABASE_HOST = os.getenv('POSTGRES_HOST', 'bd-container')  # Nombre del contenedor PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#Funcion para verificar la conexión a la base de datos
def wait_for_db(max_retries=5, delay=3):
    retries = 0
    while retries < max_retries:
        try:
            db.session.execute('SELECT 1')  # Comprobando conexión a la base de datos
            print("¡Conexión a la base de datos exitosa!")
            return
        except OperationalError:
            retries += 1
            print(f"Intentando conectar a la base de datos... ({retries}/{max_retries})")
            time.sleep(delay)
    print("No se pudo conectar a la base de datos. Abortando...")
    exit(1)

# Esperar a que la base de datos esté lista antes de crear las tablas
wait_for_db()

# Modelo de notas
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)

# Ruta principal para ver las notas
@app.route('/')
def index():
    notes = Note.query.all()
    return render_template('index.html', notes=notes)

# Ruta para agregar una nueva nota
@app.route('/add', methods=['POST'])
def add_note():
    title = request.form['title']
    description = request.form['description']
    new_note = Note(title=title, description=description)
    db.session.add(new_note)
    db.session.commit()
    return redirect(url_for('index'))

# Ruta para editar una nota
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_note(id):
    note = Note.query.get_or_404(id)
    if request.method == 'POST':
        note.title = request.form['title']
        note.description = request.form['description']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', note=note)

# Ruta para eliminar una nota
@app.route('/delete/<int:id>')
def delete_note(id):
    note = Note.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)