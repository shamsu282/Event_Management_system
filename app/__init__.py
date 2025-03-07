from flask import Flask
from config.settings import Config
from config.database import db, migrate, ma
from app.auth.signup import signup_bp
from app.auth.login import login_bp
from app.auth.logout import logout_bp
from app.event.event import event_bp
from app.event.participant import participant_bp
from app.event.organizer import organizer_bp
from flask_jwt_extended import JWTManager


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    jwt = JWTManager(app)

    
    # Register Blueprints
    app.register_blueprint(signup_bp, url_prefix='/auth')
    app.register_blueprint(login_bp, url_prefix='/auth')
    app.register_blueprint(logout_bp, url_prefix='/auth')
    app.register_blueprint(event_bp,url_prefix='/event')
    app.register_blueprint(participant_bp,url_prefix='/participant')
    app.register_blueprint(organizer_bp,url_prefix='/organizer')


    
    return app
