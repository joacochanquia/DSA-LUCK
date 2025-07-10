from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import hashlib

pgp_bp = Blueprint('pgp', __name__)

@pgp_bp.route('/pgp', methods=['GET', 'POST'])
def pgp():
    session['logged_in'] = False
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == 'admin' and hashlib.sha256(password.encode()).hexdigest() == '8cf0f7e9788fe9db170f61cd3551f69541db1633ab8e3bd393c58c001a5b754b':
            session['logged_in'] = True
            return redirect(url_for('pgp.pgp_login'))
        else:
            flash('Invalid credentials. Please try again.')
    
    return render_template('pgp_info.html')

@pgp_bp.route('/pgp/login')
def pgp_login():
    if not session.get('logged_in'):
        return redirect(url_for('pgp.pgp'))
    return render_template('pgp_login.html')