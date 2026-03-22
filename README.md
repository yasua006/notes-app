# Note App


## Løsning Beskrivelse
- Template bruk ble [sane vanilla css](https://github.com/Placewith5s/sane-vanilla-css). Mindre repetisjon blir bedre
- Jeg valgte JSON for data lagring for lettere begynnelse av prosjektet. Det er veldig sannsynlig at jeg bytter til databaser, på grunn av lettere "scale"
- Flask debugging var ikke vennlig nok, derfor valgte jeg å logge viktig meldinger i en `log.txt` fil for forbedret debugging
- Jeg får bruke `requirements.txt` for både en stabil kjøring av appen og lettere installasjon av pip packages.
- For front-end, valgte jeg å bruke rammeverket vuejs via CDN. Front-end blir bedre med reactivity. CDN for å ikke trenge installasjon av vuejs.


## Kjøring Requirements
- Ny `notes.json` fil - trenges for notater lagring

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

Aktiver .venv (PowerShell):
```sh
.venv\Scripts\activate.ps1
```
Aktiver .venv (Command Prompt):
```sh
.venv\Scripts\activate.bat
```

- For Linux og andre
For å lage en ny virtuell environment:
```sh
python -m venv .venv
```

Utforsk for aktivering av Python `.venv`.

### Få med requirements
- For MacOS
```sh
pip3 freeze > requirements.txt
```

- For Windows
```sh
pip freeze > requirements.txt
```

### Få med `node_modules` (trenges ikke akkurat nå)
- (hvis nodejs er installert):
```sh
npm install
```
Hvis nodejs er ikke installert, gå til: [nodejs installering side](https://nodejs.org/en/download) og følg instruksjonene der.


## Kjøring av prosjektet
Klienten starter med serveren. For å kjøre serveren:
```sh
uvicorn main:asgi_app
```