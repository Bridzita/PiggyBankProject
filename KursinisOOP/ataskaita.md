# Taupyklës Programos Ataskaita

## 1. Ávadas

### a. Kas yra jûsø aplikacija?

Taupyklës aplikacija yra konsolës programa, skirta padëti vartotojams valdyti savo santaupas. Ji leidþia vartotojams susikurti paskyras, nustatyti taupymo tikslus, áneðti ir iðimti pinigus bei stebëti savo progresà vizualiai per gyvûno kompanionà. Aplikacija naudoja JSON failà vartotojo duomenims iðsaugoti, uþtikrinant, kad informacija iðlieka tarp sesijø.

### b. Kaip paleisti programà?

1.  Ásitikinkite, kad turite ádiegtà Python 3.x.
2.  Iðsaugokite visus pateiktus Python failus (`Design.py`, `KursinisOOP.py`, `models.py`, `system.py`, `storage.py`) ir failà `users.json` tame paèiame aplanke.
3.  Atidarykite terminalà arba komandinæ eilutæ ir eikite á aplankà, kuriame yra failai.
4.  Paleiskite programà vykdydami komandà: `python KursinisOOP.py`

### c. Kaip naudotis programa?

1.  Paleidus programà, bus parodytas meniu su ðiomis parinktimis:
    * `1. Pridëti naujà vartotojà`
    * `2. Rasti vartotojà pagal kodà`
    * `3. Ásidëti pinigø`
    * `4. Iðimti pinigø`
    * `5. Perþiûrëti vartotojo progresà`
    * `6. Iðeiti`
2.  Áveskite skaièiø, atitinkantá norimà veiksmà.
3.  Vykdykite raginimus ávesti reikiamà informacijà, pvz., vartotojo duomenis, vartotojo kodà arba pinigø sumà.
4.  Norëdami iðeiti ið programos, pasirinkite 6 parinktá.

## 2. Pagrindinë dalis / Analizë

### a. Paaiðkinkite, kaip programa apima (ágyvendina) funkcinius reikalavimus

#### OOP ramsèiai

* **Polimorfizmas:**
    * **Paaiðkinimas:** Polimorfizmas leidþia skirtingø klasiø objektus traktuoti kaip bendro tipo objektus. Ðioje aplikacijoje polimorfizmas demonstruojamas per `User` abstraktø pagrindiná klasæ ir jos poklasá `RegularUser`. `PiggyBankSystem` gali apdoroti `User` objektus, neatsiþvelgiant á jø konkretø tipà.
    * **Kodo fragmentas:**
        ```python
        # system.py
        def add_user(self, user: User):
            if not isinstance(user, User):
                raise TypeError(
                    "Pridedamas vartotojas turi bûti User tipo objektas."
                )
            # ...
        ```
    * **Panaudojimas:** `add_user` funkcija `PiggyBankSystem` klasëje priima `User` objektà. Tai leidþia sistemai pridëti bet kokio tipo vartotojà (ðiuo metu tik `RegularUser`, bet gali bûti iðplësta).

* **Abstrakcija:**
    * **Paaiðkinimas:** Abstrakcija apima sudëtingø sistemø supaprastinimà modeliuojant klases, atitinkanèias problemà, ir dirbant tinkamu detalumo lygiu. `User` klasë yra abstrakti klasë, apibrëþianti bendrà sàsajà visiems vartotojø tipams (pvz., `add_money`, `remove_money`, `get_progress`), bet paliekanti `_generate_unique_code`, `_choose_animal_type`, `to_dict` ir `from_dict` ágyvendinimà konkreèiai `RegularUser` klasei.
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

            # ... kitos abstrakèios metodai
        ```
    * **Panaudojimas:** `PiggyBankSystem` naudotojai sàveikauja su `User` objektais per tokius metodus kaip `deposit_money`, neávesdami á konkreèias operacijø atlikimo detales `RegularUser`.

* **Paveldimumas:**
    * **Paaiðkinimas:** Paveldimumas leidþia naujoms klasëms perimti esamø klasiø savybes ir metodus. `RegularUser` klasë paveldi ið `User` klasës. Tai sukuria "yra-a" ryðá (`RegularUser` yra `User`). `RegularUser` gauna visà pagrindinæ vartotojo funkcionalumà ir prideda savo specifinius ágyvendinimus.
    * **Kodo fragmentas:**
        ```python
        # models.py
        class RegularUser(User):
            def _generate_unique_code(self) -> str:
                # ... ágyvendinimas
                pass

            def _choose_animal_type(self) -> str:
                # ... ágyvendinimas
                pass

            # ...
        ```
    * **Panaudojimas:** `RegularUser` paveldi `first_name`, `last_name`, `savings_goal`, `balance` ir tokius metodus kaip `add_money` ir `remove_money` ið `User`, bet pateikia savo ágyvendinimus unikalaus kodo generavimui ir gyvûno tipo pasirinkimui.

* **Ákapsuliavimas:**
    * **Paaiðkinimas:** Ákapsuliavimas yra duomenø (atributø) ir metodø, kurie veikia su tais duomenimis, susiejimas á vienà vienetà (klasæ). Tai taip pat apima prieigos prie kai kuriø objekto komponentø apribojimà. Python kalboje ákapsuliavimas pasiekiamas per pavadinimø suteikimo taisykles (atributø prefiksavimas vienu arba dviem pabraukimais).
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
    * **Panaudojimas:** `_first_name`, `_last_name`, `_balance`, `_user_code` ir `_animal_type` atributai yra ákapsuliuoti `User` klasëje. Jie skirti pasiekiami ir modifikuojami per klasës metodus (geteriai ir seteriai, jei reikia), o ne tiesiogiai ið klasës iðorës, uþtikrinant tam tikrà duomenø apsaugos lygá.

#### Dizaino Ðablonas

* **Factory Pattern (Fabriko Ðablonas):**
    * **Paaiðkinimas:** Fabriko Ðablonas naudojamas objektams kurti nenurodant tikslios objekto, kuris bus sukurtas, klasës. `UserFactory` klasë apibûdina logikà, skirtà `User` objektams kurti. Tai leidþia lanksèiai kurti ávairiø tipø vartotojus ateityje nekeièiant kodo, kuris naudoja fabrikà jiems kurti.
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
                raise ValueError(f"Neþinomas vartotojo tipas: {user_type}")
        ```
    * **Tinkamumas:** Fabriko Ðablonas yra tinkamas, nes jis atskiria objekto kûrimo logikà nuo likusios sistemos. Jei ateityje bus pridëta naujø vartotojø tipø (pvz., PremiumUser), `UserFactory` gali bûti iðplëstas juos kurti nekeièiant kodo, kuris naudoja fabrikà vartotojams kurti. Tai suteikia lankstesná ir lengviau priþiûrimà dizainà.

#### Kompozicija ir/arba Agregacija

* **Kompozicija:**
    * **Paaiðkinimas:** Kompozicija yra stipri asociacijos forma, kai vienas objektas yra kito objekto dalis. Sudëtinis objektas negali egzistuoti be já turinèio objekto. Ðioje aplikacijoje `PiggyBankSystem` *turi* `DataStorage`. `PiggyBankSystem` priklauso nuo `DataStorage`, kad veiktø, o `DataStorage` naudojamas tik `PiggyBankSystem`.
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
    * **Panaudojimas:** `PiggyBankSystem` sudarytas ið `DataStorage` objekto. Jis sukurtas su `DataStorage` egzemplioriumi ir remiasi juo ákeliant ir iðsaugant vartotojo duomenis. Sistema negali veikti be savo duomenø saugojimo mechanizmo.

#### Skaitymas ið failo ir raðymas á failà

* **Paaiðkinimas:** Aplikacija naudoja `JsonDataStorage` vartotojo duomenims skaityti ir raðyti á JSON failà (`users.json`). Tai leidþia aplikacijai nuolat iðsaugoti vartotojo informacijà.
* **Kodo fragmentas:**
    ```python
    # storage.py
    class JsonDataStorage(DataStorage):
        def __init__(self, data_file: str = "users.json"):
            self.data_file = data_file

        def load_users(self) -> List['User']:
            # ... ákelia vartotojus ið json failo

        def save_users(self, users: List['User']):
            # ... iðsaugo vartotojus á json failà
    ```
* **Panaudojimas:** `load_users` metodas nuskaito vartotojo duomenis ið JSON failo, kai paleidþiama aplikacija, o `save_users` metodas áraðo vartotojo duomenis á failà, kai atliekami pakeitimai (pvz., pridedamas vartotojas, áneðami pinigai).

#### Testavimas

* **Paaiðkinimas:** Pagrindinis aplikacijos funkcionalumas yra padengtas vienetiniais testais naudojant `unittest` karkasà. Testai pateikiami `models`, `system`, `storage` ir `Design` moduliams.
* **Failai:** `test_models.py`, `test_system.py`, `test_storage.py`, `test_Design.py`
* **Panaudojimas:** Testai uþtikrina, kad atskiri aplikacijos komponentai veiktø taip, kaip tikëtasi, apimant tokius atvejus kaip vartotojo kûrimas, duomenø validavimas, piniginës operacijos ir duomenø saugojimas.

#### Kodo stilius

* **Paaiðkinimas:** Kodas atitinka PEP 8 stiliaus gaires, skatinantá skaitomumà ir nuoseklumà. Tai apima tinkamà átraukimà, pavadinimø suteikimo taisykles, eiluèiø ilgio apribojimus ir tarpø naudojimà.
* **Árankiai/Linteriai (Nëra aiðkiai kode, bet numanoma):** Nors kode nëra, árankiai, tokie kaip `pylint` arba `flake8`, galëtø bûti naudojami PEP 8 atitikèiai uþtikrinti.
* **Panaudojimas:** Nuoseklus stilius palengvina kodo supratimà ir prieþiûrà tiek originaliam kûrëjui, tiek kitiems.

## 3. Rezultatai ir Apibendrinimas

### a. Rezultatai

* Aplikacija sëkmingai valdo vartotojø paskyras, leidþiant kurti, gauti ir modifikuoti vartotojo duomenis.
* Vartotojo duomenys yra nuolat saugomi JSON faile, uþtikrinant, kad duomenys iðlieka tarp sesijø.
* Programa suteikia pagrindinæ komandinës eilutës sàsajà vartotojo sàveikai.
* Vienetiniai testai buvo ágyvendinti siekiant patvirtinti pagrindiná aplikacijos funkcionalumà.
* Aplikacija demonstruoja pagrindiniø OOP principø ir dizaino ðablono naudojimà siekiant lankstaus ir lengvai priþiûrimo dizaino.

### b. Iðvados

Ðis projektas sukûrë funkcionuojanèià Taupyklës aplikacijà, kuri atitinka nurodytus reikalavimus. Aplikacija efektyviai naudoja OOP principus, dizaino ðablonà ir failø ávestá/iðvestá, kad suteiktø pagrindinæ vartotojo santaupø valdymo sistemà. Vienetiniø testø naudojimas padidina kodo patikimumà. Taip pat manau jei ðis projektas bûtø ágyvendintas sulauktu daug dëmesio ið jaunimo pusës.

### c. Kaip bûtø galima iðplësti jûsø aplikacijà?

* **Grafinë Vartotojo Sàsaja (GUI):** Vietoj komandinës eilutës sàsajos, galëtø bûti sukurta GUI, kad naudotojo patirtis bûtø patogesnë.
* **Daugiau Vartotojø Tipø:** Aplikacija galëtø bûti iðplësta, kad palaikytø skirtingus vartotojø tipus (pvz., Premium vartotojai su papildomomis funkcijomis).
* **Duomenø Bazës Integracija:** Didesnëms aplikacijoms duomenø bazë galëtø bûti naudojama vietoj JSON failo, kad bûtø efektyvesnis duomenø saugojimas ir gavimas.
* **Iðplëstinë Analitika:** Aplikacija galëtø apimti funkcijas, suteikianèias vartotojams iðsamesnæ informacijà apie jø taupymo áproèius, pvz., diagramas ir grafikus.
* **Tinklo Funkcionalumas:** Aplikacija galëtø bûti iðplësta, kad keli vartotojai galëtø pasiekti savo paskyras ið skirtingø árenginiø.