﻿#### CodeMe Python Zaawansowany
## Projekt internetowej biblioteki

#### Podsumowanie
Aplikacja biblioteki służy użytkownikom do zarządzania zasobami, zamawiania pozycji oraz sprawdzania stanu konta.

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

#### Backend
- server Flask
  - https://flask.palletsprojects.com/en/1.1.x/
- dane zapisane w SQLite3
  - https://flask.palletsprojects.com/en/1.1.x/tutorial/database/
- szablony Jinja2
  - https://jinja.palletsprojects.com/en/2.11.x/templates/