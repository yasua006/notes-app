# Notes App


## Løsning Beskrivelse
- Template bruk ble [sane vanilla css](https://github.com/Placewith5s/sane-vanilla-css). Mindre repetisjon blir bedre
- Jeg valgte JSON for data lagring, lettere begynnelse av prosjektet. Jeg har bytt til databaser og mariadb var valget - det er 100% open-source
- Flask debugging var ikke vennlig nok, derfor valgte jeg å logge viktig meldinger i en `log.txt` fil for forbedret debugging
- Jeg får bruke `requirements.txt` for både en stabil kjøring av appen og lettere installasjon av pip packages


## Kjøring Requirements (For Oppdateringer av Koden)
- Ny log.txt for å unngå `log_file` relatert feil meldinger

### Få med Python virtuell environment (`.venv`)
Vi lager og bruker Python virtuell environment for å unngå konflikter med globale pip packages.

- For MacOS

For å lage en ny virtuell environment:
```sh
python3 -m venv .venv
```

Aktiver `.venv`:
```sh
source .venv/bin/activate
```
Alternativt aktivasjon av `.venv`, kan vi skrive . istedenfor source, hvis Bash finnes på MacOS-en:
```sh
. .venv/bin/activate
```

- For Windows

For å lage en ny virtuell environment:
```sh
python -m venv .venv
```

Enten, aktiver .venv på PowerShell:
```sh
.venv\Scripts\activate.ps1
```

eller på Command Prompt:
```sh
.venv\Scripts\activate.bat
```

- For Linux og andre

For å lage en ny virtuell environment:
```sh
python -m venv .venv
```

Utforsk for aktivering av Python `.venv` på Linux.

### Få med requirements
- For MacOS
```sh
pip3 install -r requirements.txt
```

- For Windows og andre
```sh
pip install -r requirements.txt
```

### Få med `node_modules` (trenges ikke akkurat nå)
- (hvis nodejs er installert):
```sh
npm install
```
Hvis nodejs er ikke installert, gå til: [nodejs installering side](https://nodejs.org/en/download) og følg instruksjonene der.


## Kjøring av prosjektet
Vi trenger å installere og starte en lokal mariadb server for å kunne kjøre appen. Det er hva prosjektet bruker for data.

**For MacOS:** `brew install mariadb mariadb-connector-c`
> [!IMPORTANT]
> maridb-connector-c også

**For Windows:** følg denne guiden: [how to install configure mariadb on windows](https://www.geeksforgeeks.org/mariadb/how-to-install-configure-mariadb-on-windows/)

Start den lokale serveren:
```sh
uvicorn main:asgi_app
```


## API bruk
### GET /notes
Vis alle notater fant i databasen din.

### GET /todos
Vis alle TODOs fant i databasen din.

### POST /add-note
Opprett en ny notat i databasen din som inneholder en tittel og en beskrivelse.

- Tittelen og beskrivelsen - ikke tom
- Tittelen og beskrivelsen - maks. 255 karakterer

### POST /add-todo
Opprett en ny todo i databasen din som inneholder en tittel, en beskrivelse, og om oppgaven er ferdig.

- Tittelen og beskrivelsen - det samme som [/add-note seksjon](#post-add-note)
- Oppgave boolean - ikke tom

### DELETE /delete-note
Fjern en notat med tilhørende ID (query strings).

### DELETE /delete-todo
Fjern TODO med tilhørende ID (query strings).