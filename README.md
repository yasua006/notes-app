# Notes App


## Løsning Beskrivelse
- Template bruk ble [sane vanilla css](https://github.com/Placewith5s/sane-vanilla-css). Mindre repetisjon blir bedre
- Jeg valgte JSON for data lagring, lettere begynnelse av prosjektet. Jeg har bytt til databaser og mariadb var valget - det er 100% open-source
- Flask debugging var ikke vennlig nok, derfor valgte jeg å logge viktig meldinger i en `log.txt` fil for forbedret debugging
- Jeg får bruke `requirements.txt` for både en stabil kjøring av appen og lettere installasjon av pip packages


## Kjøring Requirements (For Oppdateringer av Koden)

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
uvicorn main:asgi_app
```


## API bruk
JSON blir resultatet som i en vanlig API. For å gjøre POST requests, må det være form encoding - det er fra serveren vårt prøver å få. Det reste av requests er query strings.

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

### PATCH /patch-note
Rediger en eksisterende notat i databasen din (query strings).

**Så lenge minst en av disse blir redigert:**
- Tittelen og beskrivelsen - det samme som [/add-note seksjon](#post-add-note)

### PATCH /patch-todo
Rediger en eksisterende TODO i databasen din (query strings).

**Så lenge minst en av disse blir redigert:**
- Tittelen og beskrivelsen - det samme som [/add-note seksjon](#post-add-note)
- Oppgave boolean - det samme som [/add-todo](#post-add-todo)

### DELETE /delete-note
Fjern en notat med tilhørende ID fant i databasen din (query strings).

### DELETE /delete-todo
Fjern TODO med tilhørende ID fant i databasen din (query strings).


## Hvordan Starte En Ny App Server
Vi bruker Render for å hoste vårt app server. Det er lett å bruke.

For å starte en ny server (inkluderer klienten):
1. Logge deg inn eller registrer deg en ny gratis bruker
- Registrer deg der: [Render register](https://dashboard.render.com/register)
- Eller logge deg inn: [Render login](https://dashboard.render.com/login)

2. Lag en ny web service
- [Render web service](https://dashboard.render.com/web/new)

3. For public repository
- Gå til 'Public Git Repository':
![Showing render new web service section](render_new_web_service_section.png)

4. Fylle inn alt du trenger:
- Language: Python 3

Scroll litt nede for å se "Build Command" og "Start Command". De skal være sånn:
- Build Command: `npm install && pip install -r requirements.txt`
- Start Command: `uvicorn main:asgi_app`

- Instance Type: husk å velge "Free", fordi valget er "Starter" som default og "Starter" er ikke gratis.

Scroll litt nede for å se "Environment Variables". Her skal du taste inn verdiene som du bruker for databasen:
host: verdi her
port: verdi her
username: verdi her (brukernavn til database brukeren du lagde i stad)
password: verdi her
db_name: verdi her (navnet til databasen du lagde i stad)

> [!NOTE]
> "verdi her" er placeholder, bytt til dine env. variabel verdier
> host skal ikke være "localhost" i produksjon