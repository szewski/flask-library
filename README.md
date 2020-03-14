#### CodeMe Python Zaawansowany
## Projekt internetowej biblioteki

#### Podsumowanie
Aplikacja biblioteki służy użytkownikom do zarządzania zasobami, zamawiania pozycji oraz sprawdzania stanu konta.

#### Możliwości aplikacji:
- rejestracja
- logowanie
- podział na użytkowników:
  - Guest side
    - przeglądanie

  - User side
    - przeglądanie
    - zamawianie
    - sprawdzenie stanu konta
    - przedłużenie wypożyczenia (bonus)

  - Admin side
    - przeglądanie
    - podgląd stanu konta użytkowników
    - akceptowanie zamówienia - wypożyczenie przygotowane (bonus)
    - akceptacja przedłużenia wypożyczenia (bonus)
    - dodawanie nowych pozycji
    - edytowanie pozycji

#### Backend
- server Flask
  - https://flask.palletsprojects.com/en/1.1.x/
- dane zapisane w SQLite3
  - https://flask.palletsprojects.com/en/1.1.x/tutorial/database/
- szablony Jinja2
  - https://jinja.palletsprojects.com/en/2.11.x/templates/