import unittest
import os
from piggybank import PiggyBankSystem, RegularUser, JsonDataStorage


class TestPiggyBankSystem(unittest.TestCase):
    def setUp(self):
        self.data_storage = JsonDataStorage("test_users.json")
        if os.path.exists("test_users.json"):
            os.remove("test_users.json")
        self.system = PiggyBankSystem(self.data_storage)

    def test_add_user(self):
        user = RegularUser("Test", "User", 100)
        self.system.add_user(user)
        self.assertEqual(len(self.system.users), 1)

    def test_add_duplicate_user(self):
        user1 = RegularUser("Test", "User", 100)
        self.system.add_user(user1)
        user2 = RegularUser("Test", "User", 200)
        with self.assertRaises(ValueError):
            self.system.add_user(user2)

    def test_find_user(self):
        user = RegularUser("Find", "Me", 50)
        self.system.add_user(user)
        found_user = self.system.find_user(user.user_code)
        self.assertEqual(found_user.first_name, "Find")

    def test_find_nonexistent_user(self):
        with self.assertRaises(ValueError):
            self.system.find_user("NONEXISTENT")

    def test_save_and_load_users(self):
        user1 = RegularUser("Save", "One", 75)
        user2 = RegularUser("Load", "Two", 120)
        self.system.add_user(user1)
        self
