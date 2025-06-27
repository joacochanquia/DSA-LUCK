from flask import Blueprint, render_template, request
from sqlalchemy import create_engine, text
import os

sqli_bp = Blueprint('sqli', __name__)

# Configuración de la base de datos usando variables de entorno o valores por defecto
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

@sqli_bp.route('/sqli', methods=['GET'])
def sqli():
    return render_template('sqli_info.html')

@sqli_bp.route('/sqli/database', methods=['GET'])
def sqli_database():
    results = None
    error = None
    search = request.args.get('search')
    if search:
        try:

            # VALIDACIÓN ADICIONAL: Solo permitir números enteros
            if not search.isdigit():
                error = "Solo se permiten números enteros para el ID"
                return render_template('sqli_example.html', results=results, error=error)
            
            conn = get_connection()
            
            # CORREGIDO: Usar consulta parametrizada para prevenir SQL Injection
            # En lugar de concatenar directamente, usamos parámetros seguros
            query = text("SELECT * FROM subjects WHERE id = :search_id")
            result = conn.execute(query, {'search_id': int(search)}).fetchall()
            
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
            error = f"Error en la consulta: {str(e)}"
    return render_template('sqli_example.html', results=results, error=error)
