import unittest
from app import app, db
from models import User

class UserRoutesTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    # Exemples de tests pour chaque route
    def test_get_current_user_unauthorized(self):
        response = self.app.get('/@me')
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()
