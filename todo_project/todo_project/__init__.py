from dotenv import load_dotenv
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

# Carrega as variáveis do arquivo .env
load_dotenv()

# Define o caminho do diretório base
basedir = os.path.abspath(os.path.dirname(__file__))

# Inicializa a aplicação Flask
app = Flask(__name__)

# Configura o banco de dados usando SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'site.db')

# Carrega o SECRET_KEY da variável de ambiente
secret_key = os.getenv('SECRET_KEY')
app.config['SECRET_KEY'] = secret_key

# Inicializa o SQLAlchemy com a aplicação
db = SQLAlchemy(app)

# Configura o Login Manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'danger'

# Inicializa o Bcrypt para hashing de senhas
bcrypt = Bcrypt(app)

# Importa as rotas no final para evitar problemas de importação circular
from todo_project import routes