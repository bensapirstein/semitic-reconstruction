import argparse
import time
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import tqdm

ignore_cogs = [1483, 661, 494]
ignore_words = {
    "Ugaritic": [4104,],
}
fix_words = [
    ("PS", 261, "*wŝˀ̣", "wṣ̂ˀ"),
]
def fetch_page(cog_id):
    url = "http://sed-online.ru/reconstructions/%s" % cog_id
    res = requests.get(url)
    res.raise_for_status()  # Raise an HTTPError for bad requests
    return res.text


def extract_cognates(soup, cog_id):
    entries = []

    # add reconstruction as first row
    title = soup.find("div", {"class": "col-md-8 col-xs-6"})
    lang, word = title.parent.find_all("div")
    lang = lang.find("span", {"class": "label label-info"}).text.strip()
    ipa, concept = word.h1.contents[0].split(" - ")
    ipa = ipa.strip()
    concept = concept.strip()
    try:
        note = word.h1.contents[1].text.strip()
    except IndexError:
        note = ""
    reconstruction_entry = {
        "ID": None,
        "DOCULECT": lang.strip(),
        "CONCEPT": concept.strip(),
        "VALUE": ipa.strip(),
        "TOKENS": None,
        "NOTE": note.strip(),
        "COGID": cog_id,
    }
    entries.append(reconstruction_entry)

    content_div = soup.find("div", {"id": "reconstruction_words"})
    if content_div:
        # extract proto-semitic reconstruction
        rows = content_div.find_all("div", {"class": "row"})
        for row in rows:
            lang, word = row.find_all("span", {"class": "h3"})
            lang = lang.find("span", {"class": "label label-info"}).text.strip()
            word_id = word.find("a")["href"].split("/")[-1]
            ipa = word.find("a").text.strip()
            concept = word.contents[2].replace("-", "").strip()
            try:
                note = word.contents[3].text.strip()
            except IndexError:
                note = ""

            if word_id in ignore_words.get(lang, []):
                continue
            # Add to entry dictionary with the language as the key
            word_entry = {
                "ID": word_id,
                "DOCULECT": lang,
                "CONCEPT": concept,
                "VALUE": ipa,
                "TOKENS": None,
                "NOTE": note,
                "COGID": cog_id,
                }
            entries.append(word_entry)

    return entries


def scrape_cognate(cog_id):
    html_content = fetch_page(cog_id)
    soup = bs(html_content, "html.parser")
    return extract_cognates(soup, cog_id)


def get_cognates(ids, debug_count=None):
    entries = []
    if debug_count is None:
        debug_count = len(ids)
    for i, cog_id in tqdm.tqdm(enumerate(ids), total=len(ids)):
        try:
            entry = scrape_cognate(cog_id)
            entries.extend(entry)
        except Exception as e:
            print(f"Entry {cog_id} failed - {e}")
            time.sleep(0.2)
        if i == debug_count:
            break
    return entries


def main():
    parser = argparse.ArgumentParser(description='Fetch cognates from sed-online.ru')
    parser.add_argument('--debug', type=int, help='Number of cognates to fetch in debug mode')
    args = parser.parse_args()

    reconstruction_max_id = 2153
    cog_ids = range(1, reconstruction_max_id)
    cog_ids = [x for x in cog_ids if x not in ignore_cogs]
    if args.debug:
        entries = get_cognates(cog_ids, debug_count=args.debug)
    else:
        entries = get_cognates(cog_ids)
    df = pd.DataFrame(entries)
    df.to_csv("sed.tsv", sep='\t', encoding="utf-8", index=False)


if __name__ == '__main__':
    main()
