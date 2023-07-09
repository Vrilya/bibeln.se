import re
from bs4 import BeautifulSoup, NavigableString, Tag
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
import json

# Definiera URL:en
url = "http://www.folkbibeln.net/"

# Skapa en ordbok för att lagra resultaten
bible = {"Bibeln": {}}

# Ladda böcker och kapitel från en JSON-fil
with open('bibelboker.json', 'r', encoding='utf-8') as f:
    books_and_chapters = json.load(f)

# Ställ in Firefox-alternativ för headless-läge (utan grafiskt användargränssnitt)
options = webdriver.FirefoxOptions()
options.headless = True

# Öppna webbläsaren
driver = webdriver.Firefox(executable_path="./geckodriver", options=options)

for testament, books in books_and_chapters.items():
    bible["Bibeln"][testament] = []
    for book, data in books.items():  # Här är 'data' en lista: [antal_kapitel, förkortning]
        print("Hämtar", book)
        book_abbreviation = data[1]  # Detta är förkortningen av boken
        book_dict = {book_abbreviation: []}  # Använder förkortningen här
        num_chapters = data[0]  # Detta är antalet kapitel i boken

        for chapter in range(1, num_chapters + 1):
            print("Kapitel", chapter)
            # Gå till URL:en
            driver.get(url)

            driver.switch_to.frame(0)

            # Vänta på att sidan ska laddas
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "currentBook")))

            # Välj boken i Bibeln
            book_select = Select(driver.find_element_by_id("currentBook"))
            book_select.select_by_visible_text(book)

            # Vänta på att sidan ska laddas
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "chapterSelect")))

            # Välj kapitlet
            chapter_select = Select(driver.find_element_by_id("chapterSelect"))
            chapter_select.select_by_visible_text(str(chapter))

            # Vänta på att sidan ska laddas
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "content")))

            # Hämta HTML-innehållet på sidan
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Ta bort alla fotnoter
            for footnote in soup.find_all('div', class_='footnote'):
                footnote.decompose()

            # Hitta alla versnummer
            verse_numbers = soup.find_all(['a', 'span'], class_='verseNumber')
            verses = []

            # Här plockar vi ut varje vers text, vers för vers
            for i in range(len(verse_numbers)):
                verse_text = ""
                last_seen = ""
                for element in verse_numbers[i].next_elements:
                    # Avbryt loopen om vi når nästa versnummer
                    if i < len(verse_numbers) - 1 and element == verse_numbers[i+1]:
                        break
                    # Avbryt loopen om vi når ett element med klassen 'contentTemp' eller ett div-element med stil 'margin-top: 80px'
                    if isinstance(element, Tag) and (element.get('class') == ['contentTemp'] or element.get('style') == 'margin-top: 80px'):
                        break
                    # Om elementet är en sträng (text), lägg till den i vers_text
                    if isinstance(element, NavigableString):
                        current_text = element.strip()
                        if last_seen != current_text:  # bara lägga till texten om den är annorlunda än den senast sedda texten
                            verse_text += current_text + " "
                            last_seen = current_text
                    # Om elementet är en tagg och inte har någon class, lägg till dess text i vers_text
                    elif isinstance(element, Tag) and not element.has_attr("class"):
                        current_text = element.get_text(strip=True)
                        if last_seen != current_text:  # bara lägga till texten om den är annorlunda än den senast sedda texten
                            verse_text += current_text + " "
                            last_seen = current_text

                verse_text = ' '.join(verse_text.split())  # ta bort eventuella dubbla mellanslag

                verse_text = re.sub(r'✱', '', verse_text)
                verse_text = re.sub(r'\s{2,}', ' ', verse_text)
                verse_text = re.sub(r'^\d+\s', '', verse_text)
                verse_text = re.sub(r'\s+\.', '.', verse_text)  # ta bort utrymme före punkter
                verse_text = re.sub(r'\s+,', ',', verse_text)  # ta bort utrymme före kommatecken
                verses.append({verse_numbers[i].get_text(strip=True): verse_text})

            chapter_dict = {"Chapter " + str(chapter): verses}
            book_dict[book_abbreviation].append(chapter_dict)
        bible["Bibeln"][testament].append(book_dict)

# Skriv resultaten till en JSON-fil
with open('bibeltext.json', 'w', encoding='utf-8') as f:
    json.dump(bible, f, ensure_ascii=False, indent=4)

# Stäng webbläsaren
driver.quit()
