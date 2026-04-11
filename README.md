# Notes App


## Løsning Beskrivelse
- Template bruk ble [sane vanilla css](https://github.com/Placewith5s/sane-vanilla-css). Mindre repetisjon blir bedre
- Jeg valgte JSON for data lagring og lettere begynnelse av prosjektet. Jeg har bytt til databaser og mariadb var valget - det er 100% open-source
- Flask debugging var ikke vennlig nok, derfor valgte jeg å logge viktig meldinger i en `log.txt` fil for forbedret debugging
- Jeg får bruke `requirements.txt` for både en stabil kjøring av appen og lettere installasjon av pip packages
- Siden prosjektet bruker ikke FastAPI, valgte jeg Postman for å legge til dokumentasjon


## Kjøring Requirements (For Oppdateringer av Koden)

### Få med Python virtuell environment (`.venv`)
Vi lager og bruker Python virtuell environment for å unngå konflikter med globale pip packages.

- For Linux og MacOS

For å lage en ny virtuell environment:
```sh
python3 -m venv .venv
```

Aktiver `.venv`:
```sh
source .venv/bin/activate
```
Alternativt aktivasjon av `.venv`, kan vi skrive . istedenfor source, hvis Bash finnes på OS-en:
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

### Få med requirements
- For Linux og MacOS
```sh
pip3 install -r requirements.txt
```

- For Windows og andre
```sh
pip install -r requirements.txt
```

### Få med `node_modules`
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

- Start mariadb på terminalen
Start mariadb servicen først:
```sh
`brew services start mariadb`
```
og etter det kjør:
```sh
mariadb
```

- Lag databasen i mariadb
`CREATE DATABASE dbnavn;`

- Lag brukeren i mariadb
`CREATE USER 'brukernavn'@'localhost' IDENTIFIED BY 'passord';`

- Gi brukeren tilgang til databasen i mariadb
`GRANT ALL PRIVILEGES ON dbnavn.* TO 'brukernavn'@'localhost';`
`FLUSH PRIVILEGES;`

- Start terminalen på nytt og logge deg inn som brukeren på terminalen.
```sh
mysql -u brukernavn -p
```

> [!NOTE]
> "brukernavn" er placeholder, bytt den til et bedre navn

**For Windows:** følg denne guiden: [how to install configure mariadb on windows](https://www.geeksforgeeks.org/mariadb/how-to-install-configure-mariadb-on-windows/)

Start den lokale serveren:
```sh
uvicorn main:asgi_app --reload
```


## API Bruk
Docs og response visualisering:
[Notes API docs](https://documenter.getpostman.com/view/53885114/2sBXitCnbe)
[Notes API demo](https://documenter.getpostman.com/view/53885114/2sBXitCnbd)


## Railway Snarveier
Disse snarveier er for hvis vi er på prosjektet og URL-en slutter med "/project/".

- Snarvei til "Shared Variables": legg til "settings/variables" på slutten av URL-en
- Snarvei til "Service Variables": fjern "settings" fra URL-en


## Hvordan Starte En Ny MariaDB Server (online)
Vi bruker Railway for å hoste MariaDB serveren. Det er lett å bruke.

1. Gå til [new template seksjon](railway.com/new/template) for å kunne velge å lage en ny prosjekt som starter med template

2. Skriv inn "mariadb" og velg det som står i bilden:
![Showing template search results for "mariadb"](images/templates_search_results_mariadb.png)

3. Klikk på "Deploy" etter på for å lage prosjektet


## Hvordan Starte En Ny App Server (online)
Vi bruker Railway igjen for å hoste vårt app server.

1. For å starte en ny server (inkluderer klienten):

- Registrer deg der eller logge deg inn: [Railway dashboard](https://railway.com/dashboard)

2. Lag en ny service i det samme prosjektet

- Trykk på "Add" i høyre siden av MariaDB prosjektet, "GitHub Repository", og velg notes app prosjektet

3. Oppdater shared variables

Python filen `config.py` leser "environment" variabler, derfor skal vi legge til "shared" variabler som Railway skal lese fra. Det er også for at MariaDB serveren kommuniserer riktig og oppdaterer dataen som den skal.

Klikk på "Add All" i høyre siden og "Deploy" i venstre siden, etter på.

![showing "Shared Variables" section result after Railway "Add" click/press](images/shared_variables_result.png)

4. Skriv inn "environment" variablene i "Shared Variables"

Bruk snarveiene for å lage "Shared Variables":
[Railway snarveier](#railway-snarveier)

Disse variabler er alltid det samme og kan derfor kopieres:
- MARIADB_HOST: mariadb.railway.internal
- MARIADB_PORT: 3306
- MARIADB_USER: railway
- MARIADB_DATABASE: railway

5. Kopier og lim inn MARIADB_PASSWORD verdien

- Passorden er auto generert og derfor trenger du å kopiere det:
![Showing hover on copy button next to MARIADB_PASSWORD in the MariaDB server project in section "Service Variables"](images/copy_generated_mariadb_password.png)
- Lim inn verdien du kopierte som skal lages i "Shared Variables":
MARIADB_PASSWORD: verdi her

> [!NOTE]
> "verdi her" er placeholder, bytt til dine env. variabel verdier
>
> host skal ikke være "localhost" i produksjon
