from abc import ABC, abstractmethod
import random
from typing import Dict


class User(ABC):

    def __init__(self, first_name: str, last_name: str,
                 savings_goal: float):
        self._validate_string_input(first_name, "Vardas")
        self._validate_string_input(last_name, "Pavardė")
        self._savings_goal = self._validate_positive_number_input(
            savings_goal, "Taupymo tikslas"
        )
        self._first_name = first_name
        self._last_name = last_name
        self._balance = 0.0
        self._user_code = self._generate_unique_code()
        self._animal_type = self._choose_animal_type()

    @staticmethod
    def _validate_string_input(value: str, field_name: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                f"{field_name} turi būti tekstas ir negali būti tuščias."
            )
        if not value.isalpha():
            raise ValueError(
                f"{field_name} turi būti sudarytas tik iš raidžių."
            )

    @staticmethod
    def _validate_positive_number_input(
            value: float, field_name: str
    ) -> float:
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError(
                f"{field_name} turi būti skaičius ir didesnis už 0."
            )
        return value

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    @property
    def savings_goal(self):
        return self._savings_goal

    @property
    def balance(self):
        return self._balance

    @property
    def user_code(self):
        return self._user_code

    @property
    def animal_type(self):
        return self._animal_type

    @abstractmethod
    def _generate_unique_code(self) -> str:
        pass

    @abstractmethod
    def _choose_animal_type(self) -> str:
        pass

    def add_money(self, amount: float):
        self._balance += self._validate_positive_number_input(
            amount, "Pridedama suma"
        )

    def remove_money(self, amount: float):
        amount = self._validate_positive_number_input(
            amount, "Pašalinama suma"
        )
        if amount > self._balance:
            raise ValueError("Nepakankamai lėšų sąskaitoje.")
        self._balance = max(0.0, self._balance - amount)

    def get_progress(self) -> float:
        return min(100.0, (self._balance / self._savings_goal) * 100)

    @abstractmethod
    def to_dict(self) -> Dict:
        pass

    @staticmethod
    @abstractmethod
    def from_dict(data: Dict) -> 'User':
        pass


class RegularUser(User):

    def _generate_unique_code(self) -> str:
        return (
            f"{self.first_name[0]}{self.last_name[0]}"
            f"{random.randint(1000, 9999)}"
        )

    def _choose_animal_type(self) -> str:
        return random.choice(["cat", "dog", "fox"])

    def to_dict(self) -> Dict:
        return {
            "type": "regular",
            "first_name": self.first_name,
            "last_name": self.last_name,
            "savings_goal": self.savings_goal,
            "balance": self.balance,
            "user_code": self.user_code,
            "animal_type": self.animal_type
        }

    @staticmethod
    def from_dict(data: Dict) -> 'RegularUser':
        if not isinstance(data, dict):
            raise TypeError("Vartotojo duomenys neatitinka.")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        savings_goal = data.get("savings_goal")
        balance = data.get("balance", 0.0)
        user_code = data.get("user_code")
        animal_type = data.get("animal_type")
        user = RegularUser(first_name, last_name, savings_goal)
        user._balance = balance
        user._user_code = user_code
        user._animal_type = animal_type
        return user
