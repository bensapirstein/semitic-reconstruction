import pandas as pd
from pathlib import Path

def split_values(sed):
    # split the value column by "/", ",", and " " and explode the resulting list
    sed = sed.assign(VALUE=sed.VALUE.str.split(r'[,/ ]')).explode('VALUE')
    # strip the whitespace from the value column, remove empty strings
    sed['VALUE'] = sed['VALUE'].str.strip()
    sed = sed[sed['VALUE'] != '']
    return sed

def split_concepts(sed):
    # split the concept column into multiple rows
    sed = sed.assign(CONCEPT=sed.CONCEPT.str.split(';')).explode('CONCEPT')
    # remove the leading numbers from the concept column
    sed['CONCEPT'] = sed['CONCEPT'].str.replace(r'^\s*\d+\. ', '', regex=True)
    sed['CONCEPT'] = sed['CONCEPT'].str.replace(r'^\s*[IVX]+\. ', '', regex=True)
    sed = sed.assign(CONCEPT=sed.CONCEPT.str.split(r'\([IVX]+\)')).explode('CONCEPT')
    # strip the whitespace from the concept column
    sed['CONCEPT'] = sed['CONCEPT'].str.strip()

    return sed

def filter_by_proto(sed, proto_lang="PS", num_langs=7):
    """
    Filter the SED data to only include cognates deriving from a certain proto language doculect.
    """
    data = sed.groupby('COGID').filter(lambda x: proto_lang in x['DOCULECT'].values)
    # take the first 7 most common doculects
    languages = data.groupby("DOCULECT").size().sort_values(ascending=False)
    top_languages = languages.head(num_langs).index
    data = data[data['DOCULECT'].isin(top_languages)]
    return data

if __name__ == "__main__":
    sed = pd.read_csv('../Scrapers/sed.tsv', sep='\t', dtype={'ID': str})
    # sed = split_values(sed)
    # sed = split_concepts(sed)
    sed = filter_by_proto(sed)
    sed.to_csv('cldf-datasets/kogansemitic/raw/sed.tsv', sep='\t', index=False)
