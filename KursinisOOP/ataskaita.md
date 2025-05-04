# Taupykl�s Programos Ataskaita

## 1. �vadas

### a. Kas yra j�s� aplikacija?

Taupykl�s aplikacija yra konsol�s programa, skirta pad�ti vartotojams valdyti savo santaupas. Ji leid�ia vartotojams susikurti paskyras, nustatyti taupymo tikslus, �ne�ti ir i�imti pinigus bei steb�ti savo progres� vizualiai per gyv�no kompanion�. Aplikacija naudoja JSON fail� vartotojo duomenims i�saugoti, u�tikrinant, kad informacija i�lieka tarp sesij�.

### b. Kaip paleisti program�?

1.  �sitikinkite, kad turite �diegt� Python 3.x.
2.  I�saugokite visus pateiktus Python failus (`Design.py`, `KursinisOOP.py`, `models.py`, `system.py`, `storage.py`) ir fail� `users.json` tame pa�iame aplanke.
3.  Atidarykite terminal� arba komandin� eilut� ir eikite � aplank�, kuriame yra failai.
4.  Paleiskite program� vykdydami komand�: `python KursinisOOP.py`

### c. Kaip naudotis programa?

1.  Paleidus program�, bus parodytas meniu su �iomis parinktimis:
    * `1. Prid�ti nauj� vartotoj�`
    * `2. Rasti vartotoj� pagal kod�`
    * `3. �sid�ti pinig�`
    * `4. I�imti pinig�`
    * `5. Per�i�r�ti vartotojo progres�`
    * `6. I�eiti`
2.  �veskite skai�i�, atitinkant� norim� veiksm�.
3.  Vykdykite raginimus �vesti reikiam� informacij�, pvz., vartotojo duomenis, vartotojo kod� arba pinig� sum�.
4.  Nor�dami i�eiti i� programos, pasirinkite 6 parinkt�.

## 2. Pagrindin� dalis / Analiz�

### a. Paai�kinkite, kaip programa apima (�gyvendina) funkcinius reikalavimus

#### OOP rams�iai

* **Polimorfizmas:**
    * **Paai�kinimas:** Polimorfizmas leid�ia skirting� klasi� objektus traktuoti kaip bendro tipo objektus. �ioje aplikacijoje polimorfizmas demonstruojamas per `User` abstrakt� pagrindin� klas� ir jos poklas� `RegularUser`. `PiggyBankSystem` gali apdoroti `User` objektus, neatsi�velgiant � j� konkret� tip�.
    * **Kodo fragmentas:**
        ```python
        # system.py
        def add_user(self, user: User):
            if not isinstance(user, User):
                raise TypeError(
                    "Pridedamas vartotojas turi b�ti User tipo objektas."
                )
            # ...
        ```
    * **Panaudojimas:** `add_user` funkcija `PiggyBankSystem` klas�je priima `User` objekt�. Tai leid�ia sistemai prid�ti bet kokio tipo vartotoj� (�iuo metu tik `RegularUser`, bet gali b�ti i�pl�sta).

* **Abstrakcija:**
    * **Paai�kinimas:** Abstrakcija apima sud�ting� sistem� supaprastinim� modeliuojant klases, atitinkan�ias problem�, ir dirbant tinkamu detalumo lygiu. `User` klas� yra abstrakti klas�, apibr��ianti bendr� s�saj� visiems vartotoj� tipams (pvz., `add_money`, `remove_money`, `get_progress`), bet paliekanti `_generate_unique_code`, `_choose_animal_type`, `to_dict` ir `from_dict` �gyvendinim� konkre�iai `RegularUser` klasei.
    * **Kodo fragmentas:**
        ```python
        # models.py
        class User(ABC):
            @abstractmethod
            def _generate_unique_code(self) -> str:
                pass

            @abstractmethod
            def _choose_animal_type(self) -> str:
                pass

            # ... kitos abstrak�ios metodai
        ```
    * **Panaudojimas:** `PiggyBankSystem` naudotojai s�veikauja su `User` objektais per tokius metodus kaip `deposit_money`, ne�vesdami � konkre�ias operacij� atlikimo detales `RegularUser`.

* **Paveldimumas:**
    * **Paai�kinimas:** Paveldimumas leid�ia naujoms klas�ms perimti esam� klasi� savybes ir metodus. `RegularUser` klas� paveldi i� `User` klas�s. Tai sukuria "yra-a" ry�� (`RegularUser` yra `User`). `RegularUser` gauna vis� pagrindin� vartotojo funkcionalum� ir prideda savo specifinius �gyvendinimus.
    * **Kodo fragmentas:**
        ```python
        # models.py
        class RegularUser(User):
            def _generate_unique_code(self) -> str:
                # ... �gyvendinimas
                pass

            def _choose_animal_type(self) -> str:
                # ... �gyvendinimas
                pass

            # ...
        ```
    * **Panaudojimas:** `RegularUser` paveldi `first_name`, `last_name`, `savings_goal`, `balance` ir tokius metodus kaip `add_money` ir `remove_money` i� `User`, bet pateikia savo �gyvendinimus unikalaus kodo generavimui ir gyv�no tipo pasirinkimui.

* **�kapsuliavimas:**
    * **Paai�kinimas:** �kapsuliavimas yra duomen� (atribut�) ir metod�, kurie veikia su tais duomenimis, susiejimas � vien� vienet� (klas�). Tai taip pat apima prieigos prie kai kuri� objekto komponent� apribojim�. Python kalboje �kapsuliavimas pasiekiamas per pavadinim� suteikimo taisykles (atribut� prefiksavimas vienu arba dviem pabraukimais).
    * **Kodo fragmentas:**
        ```python
        # models.py
        class User(ABC):
            def __init__(self, first_name: str, last_name: str, savings_goal: float):
                self._first_name = first_name
                self._last_name = last_name
                self._balance = 0.0
                self._user_code = self._generate_unique_code()
                self._animal_type = self._choose_animal_type()
                # ...
        ```
    * **Panaudojimas:** `_first_name`, `_last_name`, `_balance`, `_user_code` ir `_animal_type` atributai yra �kapsuliuoti `User` klas�je. Jie skirti pasiekiami ir modifikuojami per klas�s metodus (geteriai ir seteriai, jei reikia), o ne tiesiogiai i� klas�s i�or�s, u�tikrinant tam tikr� duomen� apsaugos lyg�.

#### Dizaino �ablonas

* **Factory Pattern (Fabriko �ablonas):**
    * **Paai�kinimas:** Fabriko �ablonas naudojamas objektams kurti nenurodant tikslios objekto, kuris bus sukurtas, klas�s. `UserFactory` klas� apib�dina logik�, skirt� `User` objektams kurti. Tai leid�ia lanks�iai kurti �vairi� tip� vartotojus ateityje nekei�iant kodo, kuris naudoja fabrik� jiems kurti.
    * **Kodo fragmentas:**
        ```python
        # Design.py
        class UserFactory:
            @staticmethod
            def create_user(data: Dict) -> User:
                if not isinstance(data, dict):
                    raise TypeError("Vartotojo duomenys neatitinka.")
                user_type = data.get("type", "regular")
                if user_type == "regular":
                    return RegularUser.from_dict(data)
                raise ValueError(f"Ne�inomas vartotojo tipas: {user_type}")
        ```
    * **Tinkamumas:** Fabriko �ablonas yra tinkamas, nes jis atskiria objekto k�rimo logik� nuo likusios sistemos. Jei ateityje bus prid�ta nauj� vartotoj� tip� (pvz., PremiumUser), `UserFactory` gali b�ti i�pl�stas juos kurti nekei�iant kodo, kuris naudoja fabrik� vartotojams kurti. Tai suteikia lankstesn� ir lengviau pri�i�rim� dizain�.

#### Kompozicija ir/arba Agregacija

* **Kompozicija:**
    * **Paai�kinimas:** Kompozicija yra stipri asociacijos forma, kai vienas objektas yra kito objekto dalis. Sud�tinis objektas negali egzistuoti be j� turin�io objekto. �ioje aplikacijoje `PiggyBankSystem` *turi* `DataStorage`. `PiggyBankSystem` priklauso nuo `DataStorage`, kad veikt�, o `DataStorage` naudojamas tik `PiggyBankSystem`.
    * **Kodo fragmentas:**
        ```python
        # system.py
        class PiggyBankSystem:
            def __init__(self, data_storage: DataStorage):
                if not isinstance(data_storage, DataStorage):
                    raise TypeError(
                        "Netinkamas 'data_storage' tipas"
                    )
                self.users: List[User] = []
                self.data_storage = data_storage
                self.load_users()
        ```
    * **Panaudojimas:** `PiggyBankSystem` sudarytas i� `DataStorage` objekto. Jis sukurtas su `DataStorage` egzemplioriumi ir remiasi juo �keliant ir i�saugant vartotojo duomenis. Sistema negali veikti be savo duomen� saugojimo mechanizmo.

#### Skaitymas i� failo ir ra�ymas � fail�

* **Paai�kinimas:** Aplikacija naudoja `JsonDataStorage` vartotojo duomenims skaityti ir ra�yti � JSON fail� (`users.json`). Tai leid�ia aplikacijai nuolat i�saugoti vartotojo informacij�.
* **Kodo fragmentas:**
    ```python
    # storage.py
    class JsonDataStorage(DataStorage):
        def __init__(self, data_file: str = "users.json"):
            self.data_file = data_file

        def load_users(self) -> List['User']:
            # ... �kelia vartotojus i� json failo

        def save_users(self, users: List['User']):
            # ... i�saugo vartotojus � json fail�
    ```
* **Panaudojimas:** `load_users` metodas nuskaito vartotojo duomenis i� JSON failo, kai paleid�iama aplikacija, o `save_users` metodas �ra�o vartotojo duomenis � fail�, kai atliekami pakeitimai (pvz., pridedamas vartotojas, �ne�ami pinigai).

#### Testavimas

* **Paai�kinimas:** Pagrindinis aplikacijos funkcionalumas yra padengtas vienetiniais testais naudojant `unittest` karkas�. Testai pateikiami `models`, `system`, `storage` ir `Design` moduliams.
* **Failai:** `test_models.py`, `test_system.py`, `test_storage.py`, `test_Design.py`
* **Panaudojimas:** Testai u�tikrina, kad atskiri aplikacijos komponentai veikt� taip, kaip tik�tasi, apimant tokius atvejus kaip vartotojo k�rimas, duomen� validavimas, pinigin�s operacijos ir duomen� saugojimas.

#### Kodo stilius

* **Paai�kinimas:** Kodas atitinka PEP 8 stiliaus gaires, skatinant� skaitomum� ir nuoseklum�. Tai apima tinkam� �traukim�, pavadinim� suteikimo taisykles, eilu�i� ilgio apribojimus ir tarp� naudojim�.
* **�rankiai/Linteriai (N�ra ai�kiai kode, bet numanoma):** Nors kode n�ra, �rankiai, tokie kaip `pylint` arba `flake8`, gal�t� b�ti naudojami PEP 8 atitik�iai u�tikrinti.
* **Panaudojimas:** Nuoseklus stilius palengvina kodo supratim� ir prie�i�r� tiek originaliam k�r�jui, tiek kitiems.

## 3. Rezultatai ir Apibendrinimas

### a. Rezultatai

* Aplikacija s�kmingai valdo vartotoj� paskyras, leid�iant kurti, gauti ir modifikuoti vartotojo duomenis.
* Vartotojo duomenys yra nuolat saugomi JSON faile, u�tikrinant, kad duomenys i�lieka tarp sesij�.
* Programa suteikia pagrindin� komandin�s eilut�s s�saj� vartotojo s�veikai.
* Vienetiniai testai buvo �gyvendinti siekiant patvirtinti pagrindin� aplikacijos funkcionalum�.
* Aplikacija demonstruoja pagrindini� OOP princip� ir dizaino �ablono naudojim� siekiant lankstaus ir lengvai pri�i�rimo dizaino.

### b. I�vados

�is projektas suk�r� funkcionuojan�i� Taupykl�s aplikacij�, kuri atitinka nurodytus reikalavimus. Aplikacija efektyviai naudoja OOP principus, dizaino �ablon� ir fail� �vest�/i�vest�, kad suteikt� pagrindin� vartotojo santaup� valdymo sistem�. Vienetini� test� naudojimas padidina kodo patikimum�. Taip pat manau jei �is projektas b�t� �gyvendintas sulauktu daug d�mesio i� jaunimo pus�s.

### c. Kaip b�t� galima i�pl�sti j�s� aplikacij�?

* **Grafin� Vartotojo S�saja (GUI):** Vietoj komandin�s eilut�s s�sajos, gal�t� b�ti sukurta GUI, kad naudotojo patirtis b�t� patogesn�.
* **Daugiau Vartotoj� Tip�:** Aplikacija gal�t� b�ti i�pl�sta, kad palaikyt� skirtingus vartotoj� tipus (pvz., Premium vartotojai su papildomomis funkcijomis).
* **Duomen� Baz�s Integracija:** Didesn�ms aplikacijoms duomen� baz� gal�t� b�ti naudojama vietoj JSON failo, kad b�t� efektyvesnis duomen� saugojimas ir gavimas.
* **I�pl�stin� Analitika:** Aplikacija gal�t� apimti funkcijas, suteikian�ias vartotojams i�samesn� informacij� apie j� taupymo �pro�ius, pvz., diagramas ir grafikus.
* **Tinklo Funkcionalumas:** Aplikacija gal�t� b�ti i�pl�sta, kad keli vartotojai gal�t� pasiekti savo paskyras i� skirting� �rengini�.