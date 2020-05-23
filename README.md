#### CodeMe Python Zaawansowany
## Projekt internetowej biblioteki

#### Podsumowanie
Flibre jest internetową aplikacja biblioteki. Użytkownicy mogą w niej wypożyczać oraz zwracać książki. Admin może dodać nowe pozycje, usunąć istniejące, edytować ustawienia użytkowników.

#### Możliwości aplikacji:
- rejestracja
- logowanie
- wyszukiwarka
- podział na użytkowników:
  - Guest side
    - przeglądanie katalogu

  - User side
    - przeglądanie katalogu
    - wypożyczenie
    - zwrot
    - sprawdzenie listy wypożyczeń
    - edycja danych profilu
    - przedłużenie wypożyczenia (bonus)

  - Admin side
    - przeglądanie katalogu
    - podgląd stanu wypożyczeń użytkowników
    - dodawanie nowych pozycji
    - edytowanie pozycji
    - usuwanie pozycji
    - edycja danych profili użytkowników
    - akceptowanie zamówienia - wypożyczenie przygotowane (bonus)
    - akceptacja przedłużenia wypożyczenia (bonus)

#### Uruchomienie
1. Zainstaluj wymagane pakiety: pip install -r requirements.txt
2. Stwórz bazę danych za pomocą src/db/db_init.py
3. Uruchom routes.py

#### Backend
- Python 3.7
- server Flask
  - https://flask.palletsprojects.com/en/1.1.x/
- dane zapisane w SQLite3
  - https://flask.palletsprojects.com/en/1.1.x/tutorial/database/
- szablony Jinja2
  - https://jinja.palletsprojects.com/en/2.11.x/templates/

#### Autor
Sebastian Januszewski, sebastian.januszewski1@