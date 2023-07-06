import json

# Din bok-mappning
book_mapping = {
    'gen': '1Mos', 'exo': '2Mos', 'lev': '3Mos', 'num': '4Mos', 'deu': '5Mos',
    'jos': 'Jos', 'jdg': 'Dom', 'rut': 'Rut', '1sa': '1Sam', '2sa': '2Sam',
    '1ki': '1Kung', '2ki': '2Kung', '1ch': '1Krön', '2ch': '2Krön', 'ezr': 'Esra',
    'neh': 'Neh', 'est': 'Est', 'job': 'Job', 'psa': 'Ps', 'pro': 'Ords',
    'ecc': 'Pred', 'sng': 'Hög', 'isa': 'Jes', 'jer': 'Jer', 'lam': 'Klag',
    'ezk': 'Hes', 'dan': 'Dan', 'hos': 'Hos', 'jol': 'Joel', 'amo': 'Amos',
    'oba': 'Obad', 'jon': 'Jona', 'mic': 'Mika', 'nam': 'Nah', 'hab': 'Hab',
    'zep': 'Sef', 'hag': 'Hag', 'zec': 'Sak', 'mal': 'Mal', 'mat': 'Matt',
    'mrk': 'Mark', 'luk': 'Luk', 'jhn': 'Joh', 'act': 'Apg', 'rom': 'Rom',
    '1co': '1Kor', '2co': '2Kor', 'gal': 'Gal', 'eph': 'Ef', 'php': 'Fil',
    'col': 'Kol', '1th': '1Thess', '2th': '2Thess', '1ti': '1Tim', '2ti': '2Tim',
    'tit': 'Tit', 'phm': 'Filem', 'heb': 'Hebr', 'jas': 'Jak', '1pe': '1Petr',
    '2pe': '2Petr', '1jn': '1Joh', '2jn': '2Joh', '3jn': '3Joh', 'jud': 'Jud',
    'rev': 'Upp', '1ma': '1Mack', '2ma': '2Mack', 'bar': 'Bar', 'dag': 'DanLXX',
    'esg': 'EstLXX', 'jdt': 'Judit', 'lje': 'JerBrev', 'man': 'Man', 'sir': 'Sir',
    'tob': 'Tobit', 'wis': 'Visd'
}

# Läs in .json-filen
with open('bibeln.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Funktion för att ersätta förkortningarna i JSON-datastrukturen
def replace_abbreviations(obj):
    if isinstance(obj, dict):
        for key, value in list(obj.items()):
            if key in book_mapping:
                obj[book_mapping[key]] = value
                del obj[key]
            replace_abbreviations(value)
    elif isinstance(obj, list):
        for item in obj:
            replace_abbreviations(item)

# Anropa funktionen för att ersätta förkortningarna
replace_abbreviations(data)

# Spara den uppdaterade JSON-filen
with open('bibel_sv.json', 'w') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)
