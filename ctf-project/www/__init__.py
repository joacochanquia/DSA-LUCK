from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Load configuration from a config file or environment variables
    app.config.from_mapping(
        SECRET_KEY='your_secret_key',
        DATABASE='path_to_your_database'
    )

    # Register blueprints for routes
    from .routes.index import index_bp
    from .routes.xss import xss_bp
    from .routes.pgp import pgp_bp
    from .routes.sqli import sqli_bp

    app.register_blueprint(index_bp)
    app.register_blueprint(xss_bp)
    app.register_blueprint(pgp_bp)
    app.register_blueprint(sqli_bp)

    return app