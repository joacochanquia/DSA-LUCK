from flask import Blueprint, render_template, request, make_response

xss_bp = Blueprint('xss', __name__)

@xss_bp.route('/xss', methods=['GET', 'POST'])
def xss():
    name = None
    if request.method == 'POST':
        name = request.form.get('name')
        response = make_response(render_template('xss.html', name=name))
        response.set_cookie('secret', '(![]+[])[+[]]+[!+[]+!+[]+!+[]+!+[]]+([][(![]+[])[+!+[]]+(!![]+[])[+[]]]+[])[!+[]+!+[]+!+[]]+[+!+[]]+(![]+[])[!+[]+!+[]]')
        return response
    return render_template('xss.html', name=None)