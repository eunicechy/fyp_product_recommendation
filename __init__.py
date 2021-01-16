from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate 
from config import Config
from elasticsearch import Elasticsearch
import logging
from logging.handlers import SMTPHandler
from logging.handlers import RotatingFileHandler
import os

# bootstrap = Bootstrap(app)
# db = SQLAlchemy(app)
# # migrate = Migrate(app,)

# #### HERE
# bootstrap = Bootstrap()
# db = SQLAlchemy()

# def create_app(config_class=Config):   
#     # ...
#     app = Flask(__name__)
#     POSTGRES = {
#     'user': 'my_user',
#     'pw': 'admin',
#     'db': 'my_database',
#     'host': 'localhost',
#     'port': '5432',
#     }
#     app.config.from_object(Config)
#     bootstrap.init_app(app)
#     with app.app_context():
#         db.init_app(app)
#         db.create_all(app=app)
#         db.reflect(app=app)
#     # db.Model.metadata.reflect(db.engine)

#     from .main import main as main_blueprint    
#     app.register_blueprint(main_blueprint)

#     app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
#         if app.config['ELASTICSEARCH_URL'] else None

#     ####### Error handling, disable in development
#     if not app.debug:
#         # send email to admin when site failure, 500
#         if app.config['MAIL_SERVER']:
#             auth = None
#             if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
#                 auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
#             secure = None
#             if app.config['MAIL_USE_TLS']:
#                 secure = ()
#             mail_handler = SMTPHandler(
#                 mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
#                 fromaddr='no-reply@' + app.config['MAIL_SERVER'],
#                 toaddrs=app.config['ADMINS'], subject='Site Failure',
#                 credentials=auth, secure=secure)
#             mail_handler.setLevel(logging.ERROR)
#             app.logger.addHandler(mail_handler)
        
#         # to maintain a log file for application
#         if not os.path.exists('logs'):
#             os.mkdir('logs')
#         file_handler = RotatingFileHandler('logs/productRecommendationSystem.log', maxBytes=10240,
#                                         backupCount=10)
#         file_handler.setFormatter(logging.Formatter(
#             '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
#         file_handler.setLevel(logging.INFO)
#         app.logger.addHandler(file_handler)

#         app.logger.setLevel(logging.INFO)
#         app.logger.info('Product Recommendation System startup')
        
#     return app 


#### UNCOMMENT HERE
app = Flask(__name__)
app.config.from_object(Config)
POSTGRES = {
    'user': 'my_user',
    'pw': 'admin',
    'db': 'my_database',
    'host': 'localhost',
    'port': '5432',
}

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)


# # for error handlers
# from app.errors import bp as errors_bp 
# app.register_blueprint(errors_bp)

app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None

# from app import routes, models,errors 
####### Error handling, disable in development
if not app.debug:
    # send email to admin when site failure, 500
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Site Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
    
    # to maintain a log file for application
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/productRecommendationSystem.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Product Recommendation System startup')

from app import routes, models, errors
