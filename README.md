# PiggyBank report

## 1. Įvadas

### Kas yra mano aplikacija?

PiggyBank aplikacija yra konsolės programa, skirta padėti vartotojams valdyti savo santaupas. Ji leidžia vartotojams susikurti paskyras, nustatyti taupymo tikslus, įnešti ir išimti pinigus bei stebėti savo progresą vizualiai per gyvūno kompanioną. Aplikacija naudoja JSON failą vartotojo duomenims išsaugoti, užtikrinant, kad informacija išlieka tarp sesijų.

### Kaip paleisti programą?

1.  Įsitikinkite, kad turite įdiegtą Python 3.x.
2.  Išsaugokite visus pateiktus Python failus (`Design.py`, `KursinisOOP.py`, `models.py`, `system.py`, `storage.py`) ir failą `users.json` tame pačiame aplanke.
3.  Atidarykite terminalą arba komandinę eilutę ir eikite į aplanką, kuriame yra failai.
4.  Paleiskite programą vykdydami komandą: `python KursinisOOP.py`

### Kaip naudotis programa?

1.  Paleidus programą, bus parodytas meniu su šiomis parinktimis:
    * `1. Pridėti naują vartotoją`
    * `2. Rasti vartotoją pagal kodą`
    * `3. Įsidėti pinigų`
    * `4. Išimti pinigų`
    * `5. Peržiūrėti vartotojo progresą`
    * `6. Išeiti`
2.  Įveskite skaičių, atitinkantį norimą veiksmą.
3.  Išbandykite visas parinktis, kad pamatytumėte kaip viskas veikia.
4.  Norėdami išeiti iš programos, pasirinkite 6 parinktį.

## 2. Pagrindinė dalis / Analizė

### Kaip programa apima (įgyvendina) funkcinius reikalavimus

#### OOP principai

* **Polimorfizmas:**
    * **Paaiškinimas:** Polimorfizmas leidžia skirtingų klasių objektus traktuoti kaip bendro tipo objektus. Šioje aplikacijoje polimorfizmas demonstruojamas per `User` abstraktų pagrindinį klasę ir jos poklasį `RegularUser`. `PiggyBankSystem` gali apdoroti `User` objektus, neatsižvelgiant į jų konkretų tipą.
    * **Kodo fragmentas:**
        ```python
        # system.py
        def add_user(self, user: User):
            if not isinstance(user, User):
                raise TypeError(
                    "Pridedamas vartotojas turi būti User tipo objektas."
                )
            # ...
        ```
    * **Panaudojimas:** `add_user` funkcija `PiggyBankSystem` klasėje priima `User` objektą. Tai leidžia sistemai pridėti bet kokio tipo vartotoją (šiuo metu tik `RegularUser`, bet gali būti išplėsta).

* **Abstrakcija:**
    * **Paaiškinimas:** Abstrakcija apima sudėtingų sistemų supaprastinimą modeliuojant klases, atitinkančias problemą, ir dirbant tinkamu detalumo lygiu. `User` klasė yra abstrakti klasė, apibrėžianti bendrą sąsają visiems vartotojų tipams (pvz., `add_money`, `remove_money`, `get_progress`), bet paliekanti `_generate_unique_code`, `_choose_animal_type`, `to_dict` ir `from_dict` įgyvendinimą konkrečiai `RegularUser` klasei.
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

            # ... kitos abstrakčios metodai
        ```
    * **Panaudojimas:** `PiggyBankSystem` naudotojai sąveikauja su `User` objektais per tokius metodus kaip `deposit_money`, neįvesdami į konkrečias operacijų atlikimo detales `RegularUser`.

* **Paveldimumas:**
    * **Paaiškinimas:** Paveldimumas leidžia naujoms klasėms perimti esamų klasių savybes ir metodus. `RegularUser` klasė paveldi iš `User` klasės. Tai sukuria "yra-a" ryšį (`RegularUser` yra `User`). `RegularUser` gauna visą pagrindinę vartotojo funkcionalumą ir prideda savo specifinius įgyvendinimus.
    * **Kodo fragmentas:**
        ```python
        # models.py
        class RegularUser(User):
            def _generate_unique_code(self) -> str:
                # ... įgyvendinimas
                pass

            def _choose_animal_type(self) -> str:
                # ... įgyvendinimas
                pass

            # ...
        ```
    * **Panaudojimas:** `RegularUser` paveldi `first_name`, `last_name`, `savings_goal`, `balance` ir tokius metodus kaip `add_money` ir `remove_money` iš `User`, bet pateikia savo įgyvendinimus unikalaus kodo generavimui ir gyvūno tipo pasirinkimui.

* **Inkapsuliavimas:**
    * **Paaiškinimas:** Inkapsuliavimas yra duomenų (atributų) ir metodų, kurie veikia su tais duomenimis, susiejimas į vieną vienetą (klasę). Tai taip pat apima prieigos prie kai kurių objekto komponentų apribojimą. Python kalboje įkapsuliavimas pasiekiamas per pavadinimų suteikimo taisykles (atributų prefiksavimas vienu arba dviem pabraukimais).
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
    * **Panaudojimas:** `_first_name`, `_last_name`, `_balance`, `_user_code` ir `_animal_type` atributai yra įkapsuliuoti `User` klasėje. Jie skirti pasiekiami ir modifikuojami per klasės metodus (geteriai ir seteriai, jei reikia), o ne tiesiogiai iš klasės išorės, užtikrinant tam tikrą duomenų apsaugos lygį.

#### Dizaino Šablonas

* **Factory Pattern (Fabriko Šablonas):**
    * **Paaiškinimas:** Fabriko Šablonas naudojamas objektams kurti nenurodant tikslios objekto, kuris bus sukurtas, klasės. `UserFactory` klasė apibūdina logiką, skirtą `User` objektams kurti. Tai leidžia lanksčiai kurti įvairių tipų vartotojus ateityje nekeičiant kodo, kuris naudoja fabriką jiems kurti.
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
                raise ValueError(f"Nežinomas vartotojo tipas: {user_type}")
        ```
    * **Tinkamumas:** Fabriko Šablonas yra tinkamas, nes jis atskiria objekto kūrimo logiką nuo likusios sistemos. Jei ateityje bus pridėta naujų vartotojų tipų (pvz., PremiumUser), `UserFactory` gali būti išplėstas juos kurti nekeičiant kodo, kuris naudoja fabriką vartotojams kurti. Tai suteikia lankstesnį ir lengviau prižiūrimą dizainą.

#### Kompozicija ir/arba Agregacija

## Objektų Sąveikos: Kompozicija ir Agregacija

Šiame skyriuje aptarsime objektų sąveikos principus, konkrečiai kompoziciją ir agregaciją, ir kaip jie yra įgyvendinti taupymo sistemos kode.

### Kompozicija

Kompozicija yra stiprus asociacijos tipas, kuriame vienas objektas (visuma) yra atsakingas už kito objekto (dalies) egzistavimą. Dalies objektas negali egzistuoti be visumos objekto.

* **Paaiškinimas:** Kompozicija apibrėžia "yra dalis" ryšį, kuriame dalis yra esminė visumai. Sunaikinus visumą, sunaikinamos ir jos dalys.
* **Kodo fragmentas:**

    ```python
    # system.py
    class PiggyBankSystem:

        def __init__(self, data_storage: DataStorage):
            if not isinstance(data_storage, DataStorage):
                raise TypeError(
                    "Netinkamas 'data_storage' tipas"
                )
            self.data_storage = data_storage
            # ...
    ```

* **Panaudojimas:** `PiggyBankSystem` klasė reikalauja `DataStorage` objekto savo inicijavimui. `PiggyBankSystem` yra atsakingas už `DataStorage` objekto naudojimą duomenų išsaugojimui ir įkėlimui. Nors teoriškai `PiggyBankSystem` gali veikti su skirtingais `DataStorage` tipais, jų santykis yra gana glaudus. Jei `PiggyBankSystem` objektas būtų sunaikintas, `DataStorage` objektas, kuris buvo naudojamas išskirtinai su juo, taptų nenaudojamas šioje sistemoje. Tai atspindi kompozicijos principą, kur `DataStorage` gyvavimas yra stipriai susijęs su `PiggyBankSystem`.

### Agregacija

Agregacija yra silpnesnis asociacijos tipas, kuriame objektai yra susiję, bet jų gyvavimo ciklai yra nepriklausomi. Vienas objektas (visuma) naudoja kitą objektą (dalį), bet dalis gali egzistuoti ir už visumos ribų.

* **Paaiškinimas:** Agregacija apibrėžia "turi a" ryšį, kuriame visuma naudoja dalį, bet dalis gali egzistuoti savarankiškai.
* **Kodo fragmentas:**

    ```python
    # system.py
    class PiggyBankSystem:

        def __init__(self, data_storage: DataStorage):
            # ...
            self.users: List[User] = []
            # ...

        def add_user(self, user: User):
            # ...
            self.users.append(user)
            # ...
    ```

* **Panaudojimas:** `PiggyBankSystem` klasė valdo `User` objektų sąrašą. Tačiau `User` objektai (vartotojai) gali egzistuoti nepriklausomai nuo `PiggyBankSystem`. Vartotojo duomenys yra saugomi per `DataStorage` objektą ir išliks net jei `PiggyBankSystem` objektas bus sunaikintas. Tai rodo agregaciją: `PiggyBankSystem` naudoja `User` objektus, bet nėra atsakingas už jų gyvavimo ciklą. `User` objektai gali būti naudojami kitose sistemose arba išlikti saugykloje nepriklausomai.

#### Skaitymas iš failo ir rašymas į failą

* **Paaiškinimas:** Aplikacija naudoja `JsonDataStorage` vartotojo duomenims skaityti ir rašyti į JSON failą (`users.json`). Tai leidžia aplikacijai nuolat išsaugoti vartotojo informaciją.
* **Kodo fragmentas:**
    ```python
    # storage.py
    class JsonDataStorage(DataStorage):
        def __init__(self, data_file: str = "users.json"):
            self.data_file = data_file

        def load_users(self) -> List['User']:
            # ... įkelia vartotojus iš json failo

        def save_users(self, users: List['User']):
            # ... išsaugo vartotojus į json failą
    ```
* **Panaudojimas:** `load_users` metodas nuskaito vartotojo duomenis iš JSON failo, kai paleidžiama aplikacija, o `save_users` metodas įrašo vartotojo duomenis į failą, kai atliekami pakeitimai (pvz., pridedamas vartotojas, įnešami pinigai).

#### Testavimas

* **Paaiškinimas:** Pagrindinis aplikacijos funkcionalumas yra padengtas vienetiniais testais naudojant `unittest` karkasą. Testai pateikiami `models`, `system`, `storage` ir `Design` moduliams.
* **Failai:** `test_models.py`, `test_system.py`, `test_storage.py`, `test_Design.py`
* **Panaudojimas:** Testai užtikrina, kad atskiri aplikacijos komponentai veiktų taip, kaip tikėtasi, apimant tokius atvejus kaip vartotojo kūrimas, duomenų validavimas, piniginės operacijos ir duomenų saugojimas.

#### Kodo stilius

* **Paaiškinimas:** Kodas atitinka PEP 8 stiliaus gaires, skatinantį skaitomumą ir nuoseklumą. 
* **Įrankiai/Linteriai:** Kode buvo atliktas flake8 patikrinimas, kuris parodė, kad yra vietų, kurias galima patobulinti, kad kodas pilnai atitiktų PEP 8 stilių.
* **Panaudojimas:** Nuoseklus stilius palengvina kodo supratimą ir priežiūrą tiek originaliam kūrėjui, tiek kitiems. Taip pat lengviau randamos/pamatomos klaidų vietos.

## 3. Rezultatai ir Apibendrinimas

###  Rezultatai

* Aplikacija sėkmingai valdo vartotojų paskyras, leidžiant kurti, gauti ir modifikuoti vartotojo duomenis.
* Vartotojo duomenys yra nuolat saugomi JSON faile, užtikrinant, kad duomenys išlieka tarp sesijų.
* Programa suteikia pagrindinę komandinės eilutės sąsają vartotojo sąveikai.
* Vienetiniai testai buvo įgyvendinti siekiant patvirtinti pagrindinį aplikacijos funkcionalumą.
* Aplikacija demonstruoja pagrindinių OOP principų ir dizaino šablono naudojimą siekiant lankstaus ir lengvai prižiūrimo dizaino.

### Išvados

Šis projektas sukūrė funkcionuojančią Taupyklės aplikaciją, kuri atitinka nurodytus reikalavimus. Aplikacija efektyviai naudoja OOP principus, dizaino šabloną ir failų įvestį/išvestį, kad suteiktų pagrindinę vartotojo santaupų valdymo sistemą. Vienetinių testų naudojimas padidina kodo patikimumą. Taip pat manau jei šis projektas būtų įgyvendintas sulauktu daug dėmesio iš jaunimo pusės.

### Kaip būtų galima išplėsti jūsų aplikaciją?

* **Grafinė Vartotojo Sąsaja (GUI):** Vietoj komandinės eilutės sąsajos, galėtų būti sukurta GUI, kad naudotojo patirtis būtų patogesnė.(Pvz. tkinter)
* **Daugiau Vartotojų Tipų:** Aplikacija galėtų būti išplėsta, kad palaikytų skirtingus vartotojų tipus tokius kaip PremiumUsers arba net tėvus, kurie galėtų stebėti vaikų taupymą, jiem padėti arba pakontroliuoti..
* **Duomenų Bazės Integracija:** Didesnėms aplikacijoms duomenų bazė galėtų būti naudojama vietoj JSON failo, kad būtų efektyvesnis duomenų saugojimas ir gavimas.
* **Išplėstinė Analitika:** Aplikacija galėtų apimti funkcijas, suteikiančias vartotojams išsamesnę informaciją apie jų taupymo įpročius, pvz., diagramas ir grafikus.
