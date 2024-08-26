import pandas as pd
import json
from pathlib import Path
from pyglottolog import Glottolog
from clldutils.misc import slug

in_path = Path.cwd().parent / "sed.tsv"
out_path = Path.cwd().parent.parent / "etc" / "languages.tsv"
glotto_path = Path.cwd().parent.parent.parent.parent / "cldf" / "glottolog"
def main():
    """
    read sed.tsv link it to concepticon and write out concepts.tsv
    """
    # read file and clean column "sense"
    df = pd.read_csv(in_path, sep="\t", usecols=["DOCULECT"])

    # load from lang_to_glottocode.json
    with open("lang_to_glottocode.json") as f:
        lang_to_glottocode = json.load(f)

    # Load Glottolog from the cldfbench catalog
    glottolog = Glottolog(glotto_path)

    languages = df.DOCULECT.unique()

    ids = [lang_to_glottocode[lang] if type(lang_to_glottocode[lang]) is not list else lang_to_glottocode[lang][0]
           for lang in languages if lang in lang_to_glottocode]

    langs_obj = glottolog.languoids(ids)
    langs_obj_dict = {lang.glottocode: lang for lang in langs_obj}

    langs = []
    for lang_name in languages:
        glottocode = lang_to_glottocode[lang_name]
        if type(glottocode) is list:
            glottocode = glottocode[0]

        lang_obj = langs_obj_dict.get(glottocode, None)

        if lang_obj is None:
            langs.append({
                "ID": lang_name,
                "Name": None,
                "NameInSource": lang_name,
                "Glottocode": glottocode,
                "ISO639P3code": None,
                "Latitude": None,
                "Longitude": None,
                "Family": None,
            })
        else:
            langs.append({
                "ID": slug(lang_name),
                "Name": lang_obj.name,
                "NameInSource": lang_name,
                "Glottocode": lang_obj.glottocode,
                "ISO639P3code": lang_obj.iso,
                "Latitude": lang_obj.latitude,
                "Longitude": lang_obj.longitude,
                "Family": lang_obj.family.name if lang_obj.family else None,
            })

    langs_df = pd.DataFrame(langs)



    # counts = df.groupby('DOCULECT').size().sort_values(ascending=False)
    #
    # # create COUNT column in langs_df
    # langs_df['COUNT'] = langs_df['NameInSource'].apply(lambda x: counts.get(x, 0))
    # langs_df = langs_df.sort_values("COUNT", ascending=False)

    # Save the DataFrame to a TSV file
    langs_df.to_csv(out_path, sep="\t", index=False)



    print(f"Saved {len(langs_df)} languages to {out_path}")

if __name__ == "__main__":
    main()
