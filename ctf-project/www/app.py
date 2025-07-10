from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response
from sqlalchemy import create_engine
import hashlib
import re
import os
from datetime import datetime, timedelta

app = Flask(__name__)

# Configuración
app.secret_key = os.getenv('SECRET_KEY', 'LUCK(Let Us Cook)((secreto))')
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

# Configuración de la base de datos
db_user = os.getenv("DB_USER", "user")
db_pass = os.getenv("DB_PASS", "password")
db_host = os.getenv("DB_HOST", "db")
db_name = os.getenv("DB_NAME", "ctf")
db_port = os.getenv("DB_PORT", "3306")

def get_connection():
    connection_str = f"mysql+mysqlconnector://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(connection_str)
    conn = engine.connect()
    return conn

def detect_xss(input_string):
    if not input_string:
        return False
    
    input_lower = input_string.lower()
    
    if re.search(r'document\.', input_lower, re.IGNORECASE | re.DOTALL):
        return True
    
    return False

# ========== RUTAS ==========

# Ruta principal (index)
@app.route('/')
def index():
    return render_template('index.html')

# Rutas XSS
@app.route('/xss', methods=['GET', 'POST'])
def xss():
    name = None
    if request.method == 'POST':
        name = request.form.get('name')
        response = make_response(render_template('xss.html', name=name))
        if detect_xss(name):
            expire_date = datetime.now() + timedelta(seconds=10)
            response.set_cookie(
                'secret', 
                '(![]+[])[+[]]+[!+[]+!+[]+!+[]+!+[]]+([][(![]+[])[+!+[]]+(!![]+[])[+[]]]+[])[!+[]+!+[]+!+[]]+[+!+[]]+(![]+[])[!+[]+!+[]]',
                expires=expire_date,
                secure=True
            )
        
        return response
    return render_template('xss.html', name=None)

# Rutas PGP
@app.route('/pgp')
def pgp():
    return render_template('pgp_info.html')

@app.route('/pgp/login', methods=['GET', 'POST'])
def pgp_login():
    session['logged_in'] = False
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == 'admin' and hashlib.sha256(password.encode()).hexdigest() == '8cf0f7e9788fe9db170f61cd3551f69541db1633ab8e3bd393c58c001a5b754b':
            session['logged_in'] = True
            return redirect(url_for('pgp_profile'))
        else:
            flash('Credenciales incorrectas.', 'error')
    
    return render_template('pgp_login.html')

@app.route('/pgp/profile/1')
def pgp_profile():
    if not session.get('logged_in'):
        return redirect(url_for('pgp_login'))
    return render_template('pgp_profile.html')

# Rutas SQLI
@app.route('/sqli', methods=['GET'])
def sqli():
    return render_template('sqli_info.html')

@app.route('/sqli/database', methods=['GET'])
def sqli_database():
    results = None
    error = None
    search = request.args.get('search')
    if search:
        try:
            conn = get_connection()
            query = f"SELECT * FROM subjects WHERE id = '" + (str(search)) + "';"
            result = conn.execute(query).fetchall()
            results = [
                {
                    'id': r[0],
                    'name': r[1],
                    'code': r[2],
                    'weekly_hrs': r[3],
                    'total_hrs': r[4]
                } for r in result
            ]
            conn.close()
        except Exception as e:
            error = str(e)
    return render_template('sqli_example.html', results=results, error=error)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8888, debug=True)