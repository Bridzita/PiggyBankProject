from typing import Dict
from models import User, RegularUser


class UserFactory:

    @staticmethod
    def create_user(data: Dict) -> User:
        if not isinstance(data, dict):
            raise TypeError("Vartotojo duomenys neatitinka.")
        user_type = data.get("type", "regular")
        if user_type == "regular":
            return RegularUser.from_dict(data)
        raise ValueError(f"Nežinomas vartotojo tipas: {user_type}")
