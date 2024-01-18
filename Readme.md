# Panda 3.0
## Komentarz do projektu
To jest projekt grupowy robiony na zajęcia z Inżynierii Oprogramowania (semestr 3 AGH).
## Opis
Panda 3.0 to nowoczesny system zarządzania szkołą, który oferuje szeroki zakres funkcjonalności zarówno dla nauczycieli, 
uczniów, jak i rodziców. System umożliwia zarządzanie ocenami, planami zajęć, ogłoszeniami oraz dostarcza narzędzia
do komunikacji między użytkownikami platformy.

## Technologie
Projekt został stworzony z użyciem:
 - (Python)
 - Flask 
 - SQLAlchemy
 - HTML 
 - CSS 
 - JavaScript

## Instalacja i Uruchomienie
1. Sklonuj repozytorium
2. Zmień ścieżki w pliku konfiguracyjnym pyvenv.cfg
3. Przejdź do folderu projektu i uruchom
    ```bash pip 
    python -m pip install -r requirements.txt
4. Połącz się z bazą danych (PostreSQL)
   ```bash pip 
   database="dziennik_baza"
   user="dziennik_baza_user"
   password="MNCZoIpG5hmgoEOHbGfvd15c5Br7KZfc"
   host="dpg-cldiadbmot1c73dot240-a.frankfurt-postgres.render.com"
   port="5432"
