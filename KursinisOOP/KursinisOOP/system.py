from typing import List
from models import User
from storage import DataStorage


class PiggyBankSystem:

    def __init__(self, data_storage: DataStorage):
        if not isinstance(data_storage, DataStorage):
            raise TypeError(
                "Netinkamas 'data_storage' tipas"
            )
        self.users: List[User] = []
        self.data_storage = data_storage
        self.load_users()

    def add_user(self, user: User):
        if not isinstance(user, User):
            raise TypeError(
                "Pridedamas vartotojas turi būti User tipo objektas."
            )
        if any(
            u.first_name == user.first_name and
            u.last_name == user.last_name for u in self.users
        ):
            raise ValueError("Toks vartotojas jau egzistuoja!")
        self.users.append(user)
        self.save_users()

    def find_user(self, code: str) -> User:
        if not isinstance(code, str) or not code:
            raise ValueError(
                "Vartotojo kodas turi būti tekstas ir negali būti tuščias."
            )
        for user in self.users:
            if user.user_code == code:
                return user
        raise ValueError(f"Vartotojas su kodu '{code}' nerastas")

    def deposit_money(self, code: str, amount: float):
        user = self.find_user(code)
        user.add_money(amount)
        self.save_users()
        return user

    def withdraw_money(self, code: str, amount: float):
        user = self.find_user(code)
        user.remove_money(amount)
        self.save_users()
        return user

    def get_user_progress(self, code: str) -> User:
        return self.find_user(code)

    def save_users(self):
        self.data_storage.save_users(self.users)

    def load_users(self):
        self.users = self.data_storage.load_users()
