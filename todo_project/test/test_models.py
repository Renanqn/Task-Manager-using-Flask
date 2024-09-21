import unittest
import os
from dotenv import load_dotenv
from todo_project import app, db
from todo_project.models import User, Task  # Ajuste o caminho de importação conforme necessário

# Carregue variáveis de ambiente do arquivo .env
load_dotenv()

class TestTodoModels(unittest.TestCase):

    def setUp(self):
        # Configura o Flask app para testes
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')  # Use a variável de ambiente para o SECRET_KEY
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use banco de dados SQLite em memória para testes

        # Cria um contexto de aplicação
        self.app_context = app.app_context()
        self.app_context.push()

        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        # Limpa após cada teste
        db.session.remove()
        db.drop_all()
        self.app_context.pop()  # Pop do contexto da aplicação

    def test_user_creation(self):
        # Testa a criação de usuário
        user = User(username='testuser', password=os.getenv('PASSWORD', 'default_password'))  # Use variável de ambiente para a senha
        db.session.add(user)
        db.session.commit()

        # Recupera o usuário do banco de dados
        retrieved_user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.username, 'testuser')
        self.assertEqual(retrieved_user.password, os.getenv('PASSWORD', 'default_password'))  # Confere a senha usando a variável de ambiente
    
    def test_task_creation(self):
        # Cria um usuário e uma tarefa associada a esse usuário
        user = User(username='testuser', password=os.getenv('PASSWORD', 'default_password'))
        db.session.add(user)
        db.session.commit()

        task = Task(content='Test Task', author=user)
        db.session.add(task)
        db.session.commit()

        # Recupera a tarefa do banco de dados
        retrieved_task = Task.query.filter_by(content='Test Task').first()
        self.assertIsNotNone(retrieved_task)
        self.assertEqual(retrieved_task.content, 'Test Task')
        self.assertEqual(retrieved_task.author.username, 'testuser')

    def test_load_user(self):
        # Testa a função de carregar usuário
        user = User(username='testuser', password=os.getenv('PASSWORD', 'default_password'))
        db.session.add(user)
        db.session.commit()

        loaded_user = User.query.get(int(user.id))
        self.assertIsNotNone(loaded_user)
        self.assertEqual(loaded_user.username, 'testuser')

if __name__ == '__main__':
    unittest.main()
