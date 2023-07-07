import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from bs4 import BeautifulSoup

options = Options()
options.headless = True

def get_page_content(book, book_content, driver, chapter):
    # Vänta tills sidan laddas helt
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'bt-dbl')))

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    bible_text = soup.find('div', class_='bt-bible bt-bible-read')

    # Lägg till varje vers
    current_chapter = "Chapter " + str(chapter)
    content = []
    for verse in bible_text.find_all('div', class_='bt-dbl'):
        verse_num = verse.find('span', class_='v').text.strip()
    
        try:
            verse_div = verse.find('div', class_='bt-tc txt')
            if verse_div is None:
                verse_div = verse.find('div', class_='bt-tc po')
            if verse_div is None:
                verse_div = verse.find('div', class_='bt-tc fni')
    
            if verse_div.find('span', class_='bt-info damaged'):
                p_text = " ".join([p.text for p in verse_div.find_all('p')]).strip()
                verse_text = p_text if p_text != '' else '<SKADADVERS>'
            else:
                verse_text = verse_div.text.strip()
    
        except AttributeError:
            if 'excluded' in verse.get('class', []):
                verse_text = '<VERSSAKNAS>'
            elif 'merged' in verse.get('class', []):
                verse_text = '<SAMMANSLAGENVERS>'
            else:
                verse_text = ''

        content.append({verse_num: verse_text})

    book_content[book].append({current_chapter: content})

# Läs in bibelböckerna från bibelboker2.json
with open("bibelbocker.json", "r") as file:
    bible_books = json.load(file)

driver = webdriver.Firefox(executable_path='./geckodriver', options=options)

# Initiera strukturen
data = {"Bibeln": {"GT": [], "NT": [], "Apokr": []}}

# Loopa genom varje testament och hämta böckerna
for testament, books in bible_books.items():

    # Loopa genom varje bok och hämta kapitlen
    for book, chapters in books.items():
        book_content = {book: []}

        # Loopa genom varje kapitel och hämta verserna
        for chapter in chapters:

            # Hantera bokstavskapitel separat
            if isinstance(chapter, str):
                url = f"https://bibeln.se/visa?q={book}.{chapter}%40b2k"
                driver.get(url)
                get_page_content(book, book_content, driver, chapter)
            else:
                for i in range(1, chapter + 1):
                    url = f"https://bibeln.se/visa?q={book}.{i}%40b2k"
                    driver.get(url)
                    get_page_content(book, book_content, driver, i)

        # Lägg till boken till den rätta testamentstrukturen
        data["Bibeln"][testament].append(book_content)

# Skriv till en enda JSON-fil
with open("bibeln.json", 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

driver.quit()
