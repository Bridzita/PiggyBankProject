
import random
import json
import os
from typing import List, Dict
from abc import ABC, abstractmethod
from PIL import Image


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
            with open(self.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [UserFactory.create_user(u) for u in data]
        return []

    def save_users(self, users: List['User']):
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump([u.to_dict() for u in users], f, indent=4)


class User(ABC):
    def __init__(self, first_name: str, last_name: str, savings_goal: float):
        self.first_name = first_name
        self.last_name = last_name
        self.savings_goal = savings_goal
        self.balance = 0.0
        self.user_code = self._generate_unique_code()
        self.tree_type = self._choose_tree_type()

    @abstractmethod
    def _generate_unique_code(self) -> str:
        pass

    @abstractmethod
    def _choose_tree_type(self) -> str:
        pass

    def add_money(self, amount: float):
        self.balance += amount

    def remove_money(self, amount: float):
        self.balance = max(0.0, self.balance - amount)

    def get_progress(self) -> float:
        return min(100.0, (self.balance / self.savings_goal) * 100)

    @abstractmethod
    def to_dict(self) -> Dict:
        pass

    @staticmethod
    @abstractmethod
    def from_dict(data: Dict) -> 'User':
        pass


class RegularUser(User):
    def _generate_unique_code(self) -> str:
        return (f"{self.first_name[0]}{self.last_name[0]}"
                f"{random.randint(1000, 9999)}")

    def _choose_tree_type(self) -> str:
        return random.choice(["azuolas", "berzas", "puskis"])

    def to_dict(self) -> Dict:
        return {
            "type": "regular",
            "first_name": self.first_name,
            "last_name": self.last_name,
            "savings_goal": self.savings_goal,
            "balance": self.balance,
            "user_code": self.user_code,
            "tree_type": self.tree_type
        }

    @staticmethod
    def from_dict(data: Dict) -> 'RegularUser':
        user = RegularUser(data["first_name"], data["last_name"],
                             data["savings_goal"])
        user.balance = data["balance"]
        user.user_code = data["user_code"]
        user.tree_type = data["tree_type"]
        return user


class UserFactory:
    @staticmethod
    def create_user(data: Dict) -> User:
        user_type = data.get("type", "regular")
        if user_type == "regular":
            return RegularUser.from_dict(data)
        raise ValueError(f"Neşinomas vartotojo tipas: {user_type}")


class PiggyBankSystem:
    def __init__(self, data_storage: DataStorage):
        self.users: List[User] = []
        self.data_storage = data_storage
        self.load_users()

    def add_user(self, user: User):
        if any(u.first_name == user.first_name and
               u.last_name == user.last_name for u in self.users):
            raise ValueError("Toks vartotojas jau egzistuoja!")
        self.users.append(user)
        self.save_users()

    def find_user(self, code: str) -> User:
        for user in self.users:
            if user.user_code == code:
                return user
        raise ValueError("Vartotojas nerastas")

    def save_users(self):
        self.data_storage.save_users(self.users)

    def load_users(self):
        self.users = self.data_storage.load_users()


class TreeVisualizer:
    @staticmethod
    def show_tree(tree_type: str, progress: float):
        if progress <= 25:
            stage = "stage_1.png"
        elif progress <= 50:
            stage = "stage_2.png"
        elif progress <= 75:
            stage = "stage_3.png"
        else:
            stage = "stage_4.png"

        path = os.path.join("images", tree_type.lower(), stage)
        if os.path.exists(path):
            img = Image.open(path)
            img.show()
        else:
            print(f"Nerastas paveikslëlis: {path}")


if __name__ == "__main__":
    system = PiggyBankSystem(JsonDataStorage())

    try:
        vartotojas = RegularUser("Brigita", "Ğmaro", 100)
        system.add_user(vartotojas)
    except ValueError as e:
        print(e)
        try:
            vartotojas = system.find_user("BĞ")
        except ValueError as e:
            print(e)

    for user in system.users:
        user.add_money(25)
        print(f"Progresas: {user.get_progress():.2f}%")
        TreeVisualizer.show_tree(user.tree_type, user.get_progress())