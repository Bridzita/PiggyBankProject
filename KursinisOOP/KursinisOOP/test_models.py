import unittest
from models import RegularUser


class TestUser(unittest.TestCase):

    def test_user_creation(self):
        user = RegularUser("Ugne", "Sutkaityte", 1500.0)
        self.assertEqual(user.first_name, "Ugne")
        self.assertEqual(user.last_name, "Sutkaityte")
        self.assertEqual(user.savings_goal, 1500.0)
        self.assertEqual(user.balance, 0.0)
        self.assertIsNotNone(user.user_code)
        self.assertIn(user.animal_type, ["cat", "dog", "fox"])

    def test_validate_string_input(self):
        with self.assertRaises(ValueError):
            RegularUser._validate_string_input("", "Vardas")
        with self.assertRaises(ValueError):
            RegularUser._validate_string_input("123", "Pavarde")
        with self.assertRaises(ValueError):
            RegularUser._validate_string_input("Ugne1", "Vardas")

    def test_validate_positive_number_input(self):
        with self.assertRaises(ValueError):
            RegularUser._validate_positive_number_input(-100, "Suma")
        with self.assertRaises(ValueError):
            RegularUser._validate_positive_number_input(0, "Suma")

    def test_add_money(self):
        user = RegularUser("Ugne", "Sutkaityte", 1500.0)
        user.add_money(200.0)
        self.assertEqual(user.balance, 200.0)
        with self.assertRaises(ValueError):
            user.add_money(-50)

    def test_remove_money(self):
        user = RegularUser("Ugne", "Sutkaityte", 1500.0)
        user.add_money(300.0)
        user.remove_money(100.0)
        self.assertEqual(user.balance, 200.0)
        with self.assertRaises(ValueError):
            user.remove_money(400.0)
        user.remove_money(200)
        self.assertEqual(user.balance, 0.0)

    def test_get_progress(self):
        user = RegularUser("Ugne", "Sutkaityte", 1500.0)
        user.add_money(750.0)
        self.assertEqual(user.get_progress(), 50.0)
        user.add_money(750.0)
        self.assertEqual(user.get_progress(), 100.0)
        user.remove_money(50)
        self.assertEqual(user.get_progress(), 96.66666666666667)

    def test_to_dict(self):
        user = RegularUser("Ugne", "Sutkaityte", 1500.0)
        user_dict = user.to_dict()
        self.assertEqual(user_dict["first_name"], "Ugne")
        self.assertEqual(user_dict["last_name"], "Sutkaityte")
        self.assertEqual(user_dict["savings_goal"], 1500.0)
        self.assertEqual(user_dict["balance"], 0.0)
        self.assertEqual(user_dict["type"], "regular")
        self.assertIsNotNone(user_dict["user_code"])
        self.assertIsNotNone(user_dict["animal_type"])

    def test_from_dict(self):
        user_dict = {
            "type": "regular",
            "first_name": "Viktorija",
            "last_name": "Adomaityte",
            "savings_goal": 2000.0,
            "balance": 1000.0,
            "user_code": "VA1234",
            "animal_type": "dog"
        }
        user = RegularUser.from_dict(user_dict)
        self.assertEqual(user.first_name, "Viktorija")
        self.assertEqual(user.last_name, "Adomaityte")
        self.assertEqual(user.savings_goal, 2000.0)
        self.assertEqual(user.balance, 1000.0)
        self.assertEqual(user.user_code, "VA1234")
        self.assertEqual(user.animal_type, "dog")


if __name__ == '__main__':
    unittest.main()
