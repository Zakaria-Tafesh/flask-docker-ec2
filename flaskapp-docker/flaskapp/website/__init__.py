import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

basedir = os.path.abspath(os.path.dirname(__file__))
shared_docker = os.path.join('/', 'opt', 'shared_docker')
db = SQLAlchemy()
# DB_NAME = 'database.db'



# Get environment variables
db_user = os.environ.get('MYSQL_USER')
db_password = os.environ.get('MYSQL_PASSWORD')
db_name = os.environ.get('MYSQL_DATABASE')
secret_key = os.environ.get('SECRET_KEY')
db_host = 'mysql'  # This should match the service name in your Docker Compose file



# DB_HOST = '127.0.0.1'
DB_HOST = 'mysql'
DB_PORT = '3306'  # Assuming the default MySQL port

# The other database configuration options (username, password, database name) remain the same
DB_USER = os.getenv('MYSQL_USER')
# DB_USER = 'zak'
DB_PASSWORD = os.getenv('MYSQL_PASSWORD')
DB_NAME = os.getenv('MYSQL_DATABASE')

print(f'mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = secret_key
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(shared_docker, 'database.db')
    # Construct the database URI
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{db_user}:{db_password}@{db_host}/{db_name}'
    print(f'mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    db.init_app(app)


    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from . import models
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id_):
        return models.User.query.get(int(id_))

    with app.app_context():
        db.create_all()

    return app


# def create_database(app):
#     if not path.exists('website/' + DB_NAME):
#         db.create_all(app=app)
#         print('Created Database!')
