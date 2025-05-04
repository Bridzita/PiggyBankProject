import unittest
from unittest.mock import Mock
from models import RegularUser
from system import PiggyBankSystem
from storage import DataStorage
from typing import List


class TestPiggyBankSystem(unittest.TestCase):

    def setUp(self):
        self.mock_data_storage = Mock(spec=DataStorage)
        self.system = PiggyBankSystem(self.mock_data_storage)
        self.user1 = RegularUser("Ugne", "Sutkaityte", 1500.0)
        self.user2 = RegularUser("Viktorija", "Adomaityte", 2000.0)
        self.system.users = [self.user1, self.user2]

    def _mock_load_users(self) -> List[RegularUser]:
        return [
            RegularUser("Ugne", "Sutkaityte", 1500.0),
            RegularUser("Viktorija", "Adomaityte", 2000.0),
            RegularUser("Elinga", "Kateiva", 1800.0)
        ]

    def test_add_user(self):
        new_user = RegularUser("Elinga", "Kateiva", 1800.0)
        self.system.add_user(new_user)
        self.assertTrue(
            any(
                u.first_name == "Elinga" and
                u.last_name == "Kateiva" and
                u.savings_goal == 1800.0
                for u in self.system.users
            )
        )
        self.mock_data_storage.save_users.assert_called_once()
        with self.assertRaises(TypeError):
            self.system.add_user("not a user")
        with self.assertRaises(ValueError):
            self.system.add_user(self.user1)

    def test_find_user(self):
        found_user = self.system.find_user(self.user1.user_code)
        self.assertEqual(found_user, self.user1)
        with self.assertRaises(ValueError):
            self.system.find_user("nonexistent_code")
        with self.assertRaises(ValueError):
            self.system.find_user("")

    def test_deposit_money(self):
        self.system.deposit_money(self.user1.user_code, 250.0)
        self.assertEqual(self.user1.balance, 250.0)
        self.mock_data_storage.save_users.assert_called_once()

    def test_withdraw_money(self):
        self.user1.add_money(500.0)
        self.system.withdraw_money(self.user1.user_code, 125.0)
        self.assertEqual(self.user1.balance, 375.0)
        self.mock_data_storage.save_users.assert_called_once()
        with self.assertRaises(ValueError):
            self.system.withdraw_money(self.user1.user_code, 600)

    def test_get_user_progress(self):
        progress_user = self.system.get_user_progress(
            self.user1.user_code
        )
        self.assertEqual(progress_user, self.user1)

    def test_save_and_load_users(self):
        new_user = RegularUser("Elinga", "Kateiva", 1800.0)
        self.system.add_user(new_user)
        self.system.save_users()

        loaded_users = self.system.users[:]
        loaded_users.append(new_user)
        self.mock_data_storage.load_users.return_value = loaded_users

        self.system.load_users()

        found = False
        for user in self.system.users:
            if (
                user.first_name == new_user.first_name and
                user.last_name == new_user.last_name and
                user.savings_goal == new_user.savings_goal
            ):
                found = True
                break
        self.assertTrue(found)

    if __name__ == '__main__':
        unittest.main()
