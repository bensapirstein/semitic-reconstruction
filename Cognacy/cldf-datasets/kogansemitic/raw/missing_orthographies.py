import pandas as pd
from csvw.dsv import UnicodeDictReader
from unicodedata import normalize
import json

reconstructions_url = "http://sed-online.ru/reconstructions/"
words_url = "http://sed-online.ru/words/"

unrecognized = []

with UnicodeDictReader('../etc/orthography.tsv', delimiter="\t") as reader:
    profile = {}
    for row in reader:
        profile[normalize('NFC', row['Grapheme'])] = row['IPA']
        if row['IPA'] == '<?>':
            unrecognized.append((row['Grapheme']))

print(unrecognized)
sed = pd.read_csv('../cldf/forms.csv', dtype={'ID': str})

# create a dictionary to store the words and reconstructions for each unrecognized character, then save it as a json file
unrecognized_forms = {}
for char in unrecognized:
    unrecognized_forms[char] = []
    for _, row in sed.iterrows():
        if char in row["Form"]:
            unrecognized_forms[char].append({"word": row["Form"],
                                             "url": reconstructions_url + str(row["Cognacy"]),
                                             "lang": row["Language_ID"]})

with open('unrecognized_forms.json', 'w') as f:
    json.dump(unrecognized_forms, f)
