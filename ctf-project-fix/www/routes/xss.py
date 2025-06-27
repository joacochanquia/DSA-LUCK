from flask import Blueprint, render_template, request, make_response
import base64

xss_bp = Blueprint('xss', __name__)

def xor_encrypt(data, key):
    """Cifra datos usando XOR con una clave"""
    result = []
    for i, char in enumerate(data):
        result.append(chr(ord(char) ^ ord(key[i % len(key)])))
    return ''.join(result)

@xss_bp.route('/xss', methods=['GET', 'POST'])
def xss():
    name = None
    if request.method == 'POST':
        name = request.form.get('name')
        response = make_response(render_template('xss.html', name=name))
        
        # Cookie original
        payload = '(![]+[])[+[]]+[!+[]+!+[]+!+[]+!+[]]+([][(![]+[])[+!+[]]+(!![]+[])[+[]]]+[])[!+[]+!+[]+!+[]]+[+!+[]]+(![]+[])[!+[]+!+[]]'
        # Clave para XOR
        key = "ctf_secret_2025"
        # Cifrar con XOR
        encrypted = xor_encrypt(payload, key)
        # Codificar en base64 para que sea seguro para cookies
        encoded_cookie = base64.b64encode(encrypted.encode('latin1')).decode()
        
        response.set_cookie('secret', encoded_cookie, secure=True, httponly=True)
        return response
    return render_template('xss.html', name=None)
