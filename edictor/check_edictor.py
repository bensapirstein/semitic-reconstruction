from lingpy import *
from tabulate import tabulate

wl = Wordlist("../../supervised-reconstruction-paper/data/kogansemitic.tsv")
table = []
table += [["Languages", wl.width]]
table += [["Concepts", wl.height]]
table += [["Words", len(wl)]]
table += [["Cognates", len(wl.get_etymdict(ref="cogid"))]]
print(tabulate(table))