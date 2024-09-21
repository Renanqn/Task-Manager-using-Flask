import unittest
import os
from flask import Flask
from flask_login import LoginManager, login_user, logout_user
from dotenv import load_dotenv
from todo_project import db
from todo_project.models import User
from todo_project.forms import (
    RegistrationForm,
    LoginForm,
    UpdateUserInfoForm,
    UpdateUserPassword,
    TaskForm,
    UpdateTaskForm,
)

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

class TestForms(unittest.TestCase):

    def setUp(self):
        # Configura a aplicação Flask e o banco de dados SQLite em memória para testes
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # Usa a variável de ambiente SECRET_KEY
        if not self.app.config['SECRET_KEY']:
            raise ValueError("SECRET_KEY is not set in environment variables.")  # Garante que o SECRET_KEY está configurado
        self.app.config['WTF_CSRF_ENABLED'] = False  # Desativa o CSRF para testes
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

        # Inicializa as extensões
        self.login_manager = LoginManager(self.app)  # Configura o Flask-Login
        db.init_app(self.app)

        # Cria um contexto de aplicação
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_registration_form(self):
        # Cria um formulário de registro com dados válidos
        form = RegistrationForm(username='testuser', password=os.getenv('PASSWORD'), confirm_password=os.getenv('PASSWORD'))
        self.assertTrue(form.validate())

        # Cria um usuário no banco de dados
        user = User(username='testuser', password=os.getenv('PASSWORD'))
        db.session.add(user)
        db.session.commit()

        # Verifica se o formulário levanta um erro de validação para o nome de usuário existente
        form = RegistrationForm(username='testuser', password=os.getenv('PASSWORD'), confirm_password=os.getenv('PASSWORD'))
        self.assertFalse(form.validate())

    def test_login_form(self):
        # Cria um formulário de login com dados válidos
        form = LoginForm(username='testuser', password=os.getenv('PASSWORD'))
        self.assertTrue(form.validate())

    def test_update_user_info_form(self):
        # Simula um usuário logado
        user = User(username='testuser', password=os.getenv('PASSWORD'))
        db.session.add(user)
        db.session.commit()
        with self.app.test_request_context():
            login_user(user)

            # Formulário com um nome de usuário diferente, deve ser inválido
            form = UpdateUserInfoForm(username='existinguser')
            self.assertFalse(form.validate())

            # Formulário com o mesmo nome de usuário, deve ser válido
            form = UpdateUserInfoForm(username='testuser')
            self.assertTrue(form.validate())

            logout_user()

    def test_update_user_password_form(self):
        # Cria um formulário para alterar a senha
        form = UpdateUserPassword(old_password=os.getenv('OLD_PASSWORD'), new_password=os.getenv('NEW_PASSWORD'))
        self.assertTrue(form.validate())

    def test_task_form(self):
        # Cria um formulário de tarefa com dados válidos
        form = TaskForm(task_name='Test Task')
        self.assertTrue(form.validate())

    def test_update_task_form(self):
        # Cria um formulário de atualização de tarefa com dados válidos
        form = UpdateTaskForm(task_name='Updated Task Description')
        self.assertTrue(form.validate())

if __name__ == '__main__':
    unittest.main()
