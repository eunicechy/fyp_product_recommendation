import os

class Config(object):
  SQLALCHEMY_DATABASE_URI = 'postgresql://my_user:admin@localhost/my_database'
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SECRET_KEY = "admin"
  ELASTICSEARCH_URL = 'http://localhost:9200'
  # ELASTICSEARCH_URL='http://localhost:9200'
  MAIL_SERVER = os.environ.get('MAIL_SERVER')
  MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
  MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
  MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
  MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
  ADMINS = ['eunicechy@siswa.um.edu.my']
  PRODUCTS_PER_PAGE = 5
  SQLALCHEMY_POOL_SIZE = 20