from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    
    app.secret_key = os.getenv('SECRET_KEY', 'LUCK(Let Us Cook)((secreto))')
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    with app.app_context():
        from .routes.index import index_bp
        from .routes.xss import xss_bp
        from .routes.pgp import pgp_bp
        from .routes.sqli import sqli_bp

        app.register_blueprint(index_bp)
        app.register_blueprint(xss_bp)
        app.register_blueprint(pgp_bp)
        app.register_blueprint(sqli_bp)

    return app




if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=8888, debug=True)