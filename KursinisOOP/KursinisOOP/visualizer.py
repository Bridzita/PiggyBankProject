import os
from PIL import Image


class AnimalVisualizer:
    @staticmethod
    def show_animal(animal_type: str, progress: float):
        if not isinstance(animal_type, str) or not animal_type:
            print("Įspėjimas: Netinkamas gyvūno tipas.")
            return
        if not isinstance(progress, (int, float)):
            print("Įspėjimas: Netinkamas progresas.")
            return
        if progress < 0 or progress > 100:
            print("Įspėjimas: Progresas turi būti tarp 0 ir 100.")
            return

        if progress <= 25:
            stage = "stage_1.png"
        elif progress <= 50:
            stage = "stage_2.png"
        elif progress <= 75:
            stage = "stage_3.png"
        else:
            stage = "stage_4.png"

        path = os.path.join("images", animal_type.lower(), stage)
        if os.path.exists(path):
            try:
                img = Image.open(path)
                img.show()
            except FileNotFoundError:
                print(f"Nerastas paveikslėlis: {path}")
            except Exception as e:
                print(f"Klaida atidarant paveikslėlį: {e}")
        else:
            print(f"Nerastas paveikslėlis: {path}")
