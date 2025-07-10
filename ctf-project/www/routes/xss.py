from flask import Blueprint, render_template, request, make_response
import re
from datetime import datetime, timedelta

xss_bp = Blueprint('xss', __name__)

def detect_xss(input_string):
    if not input_string:
        return False
    
    input_lower = input_string.lower()
    
    if re.search(r'document\.', input_lower, re.IGNORECASE | re.DOTALL):
        return True
    
    return False

@xss_bp.route('/xss', methods=['GET', 'POST'])
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