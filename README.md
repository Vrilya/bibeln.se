# Projekt: Webbskrapning av Bibelverser

Jag har skapat det här pythonprojektet som ett datadrivet tillvägagångssätt för diskussioner och debatter om religion. Som ateist, finner jag det nyttigt att ha en solid förståelse för Bibeln när jag diskuterar med kristna. Långsamma webbplatser och online-resurser kan vara ett hinder för snabb referering och åtkomst till bibelverser under dessa diskussioner. För att lösa detta, har jag skrivit ett Python-skript som skrapar texten i Bibeln från https://bibeln.se. Skriptet använder Selenium och BeautifulSoup för att navigera på webbplatsen och tolka innehållet. Det lagrar denna data i en lättanvänd JSON-fil.

## Verktyg

Skriptet använder `geckodriver`, som är en proxy för att använda W3C WebDriver-kompatibla klienter för att interagera med Gecko-baserade webbläsare, i det här fallet Firefox.

`Selenium WebDriver` är ett verktyg som används för att automatisera webbläsare. Den kommunicerar med webbläsaren genom att skicka kommandon till geckodrivern. Med hjälp av WebDriver kan vi utföra olika typer av operationer på webbsidor, såsom att klicka på en knapp, skriva in text i ett fält, navigera till en annan sida, och så vidare. Den kan även användas för att hämta innehåll från webbsidor, vilket är det huvudsakliga syftet med det här skriptet.

I det här skriptet skapar vi en instans av Firefox-webbläsaren i headless-läge (dvs. utan ett grafiskt användargränssnitt) genom att ställa in `options.headless` till `True`. Sedan öppnar vi en webbsida genom att anropa `driver.get(url)` och väntar tills sidan är helt laddad innan vi fortsätter med att skrapa dess innehåll.

`BeautifulSoup` är ett Python-bibliotek för att parsa HTML och XML dokument. Det skapar ett träd av objekt från sidans innehåll, vilket gör det lättare att navigera och söka igenom det. I det här skriptet används BeautifulSoup för att hitta specifika element på sidan och extrahera den text vi är intresserade av.

## Funktionalitet

Skriptet går igenom varje bok och kapitel i Bibeln listade på webbplatsen och samlar alla verser. Den resulterande strukturen av data ser ut så här:

```plaintext
Bibeln
├── GT (Gamla testamentet)
│   ├── Bok 1
│   │   ├── Kapitel 1
│   │   │   ├── Vers 1
│   │   │   ├── Vers 2
│   │   │   └── ...
│   │   ├── Kapitel 2
│   │   └── ...
│   ├── Bok 2
│   └── ...
├── NT (Nya testamentet)
│   └── ...
└── Apokr (Apokryfer)
    └── ...
```


## Särskilda fall

Under processen stöter vi på vissa speciella fall med verser, däribland saknade, sammanslagna och skadade verser. Jag har hanterat dessa på följande sätt:

- **Saknade verser**: Verser som saknas i texten är markerade som &lt;VERSSAKNAS&gt;.
- **Sammanslagna verser**: Sammanslagna verser är markerade som &lt;SAMMANSLAGENVERS&gt;.
- **Skadade verser**: Skadade verser, där det ursprungliga innehållet inte är klart eller komplett, är markerade som &lt;SKADADVERS&gt;.

## Användning av .json-filen

Den skapade .json-filen kan användas för att snabbt söka och referera till specifika bibelverser. Dess strukturerade format gör det enkelt att navigera och hitta det du behöver. Du kan använda det för att skapa olika verktyg för att söka och analysera bibelverser på ett snabbt och effektivt sätt.
