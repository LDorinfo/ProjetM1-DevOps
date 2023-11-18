import unittest
from app import app, db

class TestApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_get_current_user_unauthorized(self):
        response = self.app.get('/@me')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, {"error": "Unauthorized"})

    def test_home_route(self):
        response = self.app.get('/home')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), 'Hello')

    def test_register_user(self):
        # Implement your registration test here
        pass

    def test_login_user(self):
        # Implement your login test here
        pass

    # Ajoutez d'autres tests pour les différentes routes de votre application

if __name__ == '__main__':
    unittest.main()
