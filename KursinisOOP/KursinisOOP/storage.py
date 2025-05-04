import json
import os
from abc import ABC, abstractmethod
from typing import List
from models import User
from Design import UserFactory


class DataStorage(ABC):

    @abstractmethod
    def load_users(self) -> List['User']:
        pass

    @abstractmethod
    def save_users(self, users: List['User']):
        pass


class JsonDataStorage(DataStorage):

    def __init__(self, data_file: str = "users.json"):
        self.data_file = data_file

    def load_users(self) -> List['User']:
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    users = [UserFactory.create_user(u) for u in data]
                    return users
            except FileNotFoundError:
                return []
            except json.JSONDecodeError:
                print(
                    "Įspėjimas: Nepavyko įkelti vartotojų iš "
                    f"'{self.data_file}'. Failas gali būti sugadintas."
                )
                return []
        return []

    def save_users(self, users: List['User']):
        if not isinstance(users, list):
            raise TypeError("Vartotojų sąrašas turi būti sąrašas.")
        for user in users:
            if not isinstance(user, User):
                raise TypeError("Sąraše turi būti tik User klasės objektai.")
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump([u.to_dict() for u in users], f, indent=4)
