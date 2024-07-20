import pandas as pd

sed = pd.read_csv("../cldf-datasets/kogansemitic/raw/sed.tsv", sep='\t', dtype={'ID': str})
forms = pd.read_csv("../cldf-datasets/kogansemitic/cldf/forms.csv", dtype={'ID': str})

sed.TOKENS = forms.Segments
sed['ID'] = sed.reset_index().index.astype(str)
sed['FORM'] = forms["Form"]
sed["ALIGNMENT"] = forms["Graphemes"]
# remove ^ and $ from the beginning and end of the alignment and strip it
sed["ALIGNMENT"] = sed["ALIGNMENT"].str.replace(r"^\^", "").str.replace(r"\$$", "").str.strip()



sed.to_csv("sed.tsv", sep="\t", index=False)
