from system import PiggyBankSystem
from storage import JsonDataStorage
from models import RegularUser
from visualizer import AnimalVisualizer


def display_menu():
    print("\n--- Piggy Bank ---")
    print("1. Pridėti naują vartotoją")
    print("2. Rasti vartotoją pagal kodą")
    print("3. Įsidėti pinigų")
    print("4. Išimti pinigų")
    print("5. Peržiūrėti vartotojo progresą")
    print("6. Išeiti")


def add_new_user(system: PiggyBankSystem):
    while True:
        first_name = input("Įveskite vartotojo vardą: ")
        try:
            RegularUser._validate_string_input(first_name, "Vardas")
            break
        except ValueError as e:
            print(e)

    while True:
        last_name = input("Įveskite vartotojo pavardę: ")
        try:
            RegularUser._validate_string_input(last_name, "Pavardė")
            break
        except ValueError as e:
            print(e)

    while True:
        savings_goal_str = input("Įveskite taupymo tikslą: ")
        try:
            savings_goal = RegularUser._validate_positive_number_input(
                float(savings_goal_str), "Taupymo tikslas"
            )
            user = RegularUser(first_name, last_name, savings_goal)
            system.add_user(user)
            print(
                "Vartotojas "
                f"{first_name} {last_name} sėkmingai pridėtas su kodu: "
                f"{user.user_code}"
            )
            break
        except ValueError as e:
            print(e)


def find_user(system: PiggyBankSystem):
    while True:
        code = input("Įveskite vartotojo kodą: ")
        try:
            user = system.find_user(code)
            print(
                "Rastas vartotojas: "
                f"{user.first_name} {user.last_name}, "
                f"Balansas: {user.balance:.2f}, "
                f"Tikslas: {user.savings_goal:.2f}, "
                f"Gyvūnas: {user.animal_type}"
            )
            break
        except ValueError as e:
            print(e)
            another_attempt = input(
                "Ar norite bandyti įvesti kodą dar kartą? (taip/ne): "
            ).lower()
            if another_attempt != 'taip':
                break


def deposit_money(system: PiggyBankSystem):
    code = input(
        "Įveskite vartotojo kodą, į kurio sąskaitą norite įnešti pinigų: "
    )
    while True:
        amount_str = input("Įveskite įnešamą sumą: ")
        try:
            amount = RegularUser._validate_positive_number_input(
                float(amount_str), "Įnešama suma"
            )
            user = system.deposit_money(code, amount)
            print(
                "Sėkmingai įnešta į vartotojo "
                f"{user.first_name} sąskaitą. "
                f"Naujas balansas: {user.balance:.2f}"
            )
            break
        except ValueError as e:
            print(e)


def withdraw_money(system: PiggyBankSystem):
    code = input(
        "Įveskite vartotojo kodą, iš kurios sąskaitos norite išimti pinigų: "
    )
    while True:
        amount_str = input("Įveskite išimamą sumą: ")
        try:
            amount = RegularUser._validate_positive_number_input(
                float(amount_str), "Išimama suma"
            )
            user = system.withdraw_money(code, amount)
            print(
                "Sėkmingai išimta iš vartotojo "
                f"{user.first_name} sąskaitos. "
                f"Naujas balansas: {user.balance:.2f}"
            )
            break
        except ValueError as e:
            print(e)


def view_progress(system: PiggyBankSystem):
    code = input("Įveskite vartotojo kodą, kurio progresą norite peržiūrėti: ")
    try:
        user = system.get_user_progress(code)
        progress = user.get_progress()
        print(
            f"Vartotojo {user.first_name} {user.last_name} "
            f"progresas: {progress:.2f}%"
        )
        AnimalVisualizer.show_animal(user.animal_type, progress)
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    data_storage = JsonDataStorage("users.json")
    system = PiggyBankSystem(data_storage)

    actions = {
        '1': add_new_user,
        '2': find_user,
        '3': deposit_money,
        '4': withdraw_money,
        '5': view_progress
    }

    while True:
        display_menu()
        choice = input("Pasirinkite veiksmą: ")

        try:
            if choice in actions:
                confirm = input(
                    "Ar tikrai norite atlikti šį veiksmą? (taip/ne): "
                ).lower()
                if confirm == 'taip':
                    actions[choice](system)
            elif choice == '6':
                print("Ačiū, kad naudojotės taupyklės sistema!")
                break
            else:
                print("Netinkamas pasirinkimas. Bandykite dar kartą.")
        except Exception as e:
            print(f"Įvyko netikėta klaida: {e}")
