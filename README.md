# Projekt: Webbskrapning av Bibelverser

Jag har skapat det här projektet som ett datadrivet tillvägagångssätt för diskussioner och debatter om religion. Som ateist, finner jag det nyttigt att ha en solid förståelse för Bibeln när jag diskuterar med kristna. Långsamma webbplatser och online-resurser kan vara ett hinder för snabb referering och åtkomst till bibelverser under dessa diskussioner. För att lösa detta, har jag skrivit ett Python-skript som skrapar texten i Bibeln från https://bibeln.se. Skriptet använder Selenium och BeautifulSoup för att navigera på webbplatsen och tolka innehållet. Det lagrar denna data i en lättanvänd JSON-fil.

## Funktionalitet

Skriptet går igenom varje bok och kapitel i Bibeln listade på webbplatsen och samlar alla verser. Den resulterande strukturen av data ser ut så här:

Bibeln
├── GT (Gamla testamentet)
│ ├── Bok 1
│ │ ├── Kapitel 1
│ │ │ ├── Vers 1
│ │ │ ├── Vers 2
│ │ │ └── ...
│ │ ├── Kapitel 2
│ │ └── ...
│ ├── Bok 2
│ └── ...
├── NT (Nya testamentet)
│ └── ...
└── Apokr (Apokryfer)
└── ...


## Särskilda fall

Under processen stöter vi på vissa speciella fall med verser, däribland saknade, sammanslagna och skadade verser. Jag har hanterat dessa på följande sätt:

- **Saknade verser**: Verser som saknas i texten är markerade som '<VERSSAKNAS>'.
- **Sammanslagna verser**: Sammanslagna verser är markerade som '<SAMMANSLAGENVERS>'.
- **Skadade verser**: Skadade verser, där det ursprungliga innehållet inte är klart eller komplett, är markerade som '<SKADADVERS>'.

## Användning av .json-filen

Den skapade .json-filen kan användas för att snabbt söka och referera till specifika bibelverser. Dess strukturerade format gör det enkelt att navigera och hitta det du behöver. Du kan använda det för att skapa olika verktyg för att söka och analysera bibelverser på ett snabbt och effektivt sätt.
