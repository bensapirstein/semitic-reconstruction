from lingpy import *
from lingpy.align.multiple import Multiple

def run(wordlist, gap="-"):
    D = {0: wordlist.columns+["alignment"]}
    for i, ids in wordlist.iter_cognates("cogid"):
        seqs = [wordlist[idx, "tokens"] for idx in ids[0]]
        seqs = [[s for s in seq if s != gap] for seq in seqs]
        msa = Multiple([[s for s in seq if s != gap] for seq in seqs])
        msa.prog_align()
        alms = [alm for alm in msa.alm_matrix]
        for idx, alm in zip(ids[0], alms):
            D[idx] = [wordlist[idx, h] for h in wordlist.columns] + [alm]

    return D
