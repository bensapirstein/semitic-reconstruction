import time

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import re


def scrape_word(word_id):
    # Use a breakpoint in the code line below to debug your script.
    res = requests.get("https://rothfarb.info/ronen/arabic/word.asp?id=%s" % word_id)
    soup = bs(res.text.encode("ISO-8859-1"), "html.parser")
    content_div = soup.find("div", {"class": "result"})
    # verified = soup.find("div", {"class": "tableH"}).text
    heb_text = content_div.find("div", {"class": "heb"}).text.strip()
    heb_parts = heb_text.split("\r\n")
    if len(heb_parts) > 1:
        heb_word, heb_comment = heb_parts
    else:
        heb_word = heb_parts[0]
        heb_comment = ""
    heb_word = heb_word.strip()
    heb_comment = heb_comment.strip()
    # heb_word, heb_comment = re.split("\((.*?)\)",heb_text)
    harm = content_div.find("div", {"class": "harm"}).text.strip()
    keter = content_div.find("span", {"class": "keter"}).text.strip()
    eng = content_div.find("div", {"class": "eng"}).text.strip()
    pos = content_div.find("div", {"class": "pos"}).text.strip()
    gender = content_div.find("div", {"class": "gender"}).text.strip()
    number = content_div.find("div", {"class": "number"}).text.strip()
    relations_div = soup.find("div", {"class": "table h2"})
    fieldsets = relations_div.find_all("fieldset")
    relations = {}
    curr_legend = ""
    for fieldset in fieldsets:
        legend = fieldset.find("legend")
        if legend is not None:
            curr_legend = ' '.join(legend.text.strip().split())
            relations[curr_legend] = []
        ref = fieldset.find("div")["onclick"]
        relations[curr_legend].append(ref)

    # return {'id': str(word_id), 'heb': heb, 'harm': harm, 'keter': keter, 'eng': eng, 'pos': pos, 'gender': gender, 'number': number}
    return {'id':word_id,'heb': heb_word, 'heb_comment' : heb_comment, 'harm': harm, 'keter': keter, 'eng': eng, 'pos': pos, 'gender': gender, 'number': number,
            'relations': relations}

def get_entries(ids):
    entries = []
    for id in ids:
        try:
            entry = scrape_word(id)
            entries.append(entry)
            print("entry %s succeeded" % id)
        except Exception as e:
            print("entry %s failed - %s" % (id, e))
            time.sleep(0.2)
    return entries

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    entries = get_entries(range(8000,9000))
    df = pd.DataFrame(entries)
    # with open("out.txt", "w", encoding='utf-8') as f:
    #     values = [",".join(d.values()) for d in entries]
    #     f.writelines(values)
    df.to_csv("dict.csv", encoding="utf-8")
