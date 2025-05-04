import unittest
import os
import json
from storage import JsonDataStorage
from models import RegularUser


class TestJsonDataStorage(unittest.TestCase):

    def setUp(self):
        self.test_file = "test_users.json"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.storage = JsonDataStorage(self.test_file)
        self.user1 = RegularUser("Ugne", "Sutkaityte", 1500.0)
        self.user2 = RegularUser("Viktorija", "Adomaityte", 2000.0)
        self.users = [self.user1, self.user2]

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_save_and_load_users(self):
        self.storage.save_users(self.users)
        loaded_users = self.storage.load_users()
        self.assertEqual(len(loaded_users), 2)
        self.assertEqual(loaded_users[0].first_name, "Ugne")
        self.assertEqual(loaded_users[1].first_name, "Viktorija")
        with self.assertRaises(TypeError):
            self.storage.save_users("not a list")
        with self.assertRaises(TypeError):
            self.storage.save_users(["not a user"])

    def test_load_users_file_not_found(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        loaded_users = self.storage.load_users()
        self.assertEqual(loaded_users, [])

    def test_load_users_invalid_json(self):
        with open(self.test_file, "w") as f:
            f.write("invalid json")
        loaded_users = self.storage.load_users()
        self.assertEqual(loaded_users, [])

    def test_save_users_correct_data(self):
        self.storage.save_users([self.user1])
        with open(self.test_file, 'r') as f:
            data = json.load(f)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['first_name'], 'Ugne')


if __name__ == '__main__':
    unittest.main()
