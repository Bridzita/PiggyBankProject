import unittest
from Design import UserFactory
from models import RegularUser


class TestUserFactory(unittest.TestCase):

    def test_create_regular_user(self):
        data = {
            "type": "regular",
            "first_name": "Ugne",
            "last_name": "Sutkaityte",
            "savings_goal": 1500.0,
            "balance": 750.0,
            "user_code": "US1234",
            "animal_type": "cat"
        }
        user = UserFactory.create_user(data)
        self.assertIsInstance(user, RegularUser)
        self.assertEqual(user.first_name, "Ugne")

    def test_create_user_invalid_type(self):
        data = {
            "type": "invalid",
            "first_name": "Viktorija",
            "last_name": "Adomaityte",
            "savings_goal": 2000.0
        }
        with self.assertRaises(ValueError):
            UserFactory.create_user(data)

    def test_create_user_invalid_data(self):
        with self.assertRaises(TypeError):
            UserFactory.create_user("not a dict")

    def test_create_user_missing_data(self):
        data = {
            "type": "regular",
            "first_name": "Elinga",
            "savings_goal": 1800.0
        }
        with self.assertRaises(ValueError):
            UserFactory.create_user(data)


if __name__ == '__main__':
    unittest.main()
