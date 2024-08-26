replacements = [
    ("*", ""),
    ("­", ""),
    ("1", ""),
    ("V̄", "-"),
    ("V", "-"),  # TODO: Implement Uncertainty (List 2023 4.2)
    ("̱V", "-"),
    ("S", "-"),
    ("Š", "-"),
    ("P", "-"),
    ("N", "-"),
    # ("S", "s/š/ŝ"), # TODO: Implement Uncertainty (List 2023 4.2)
    ("ˇ", "-"),
    ("I", "-"),
    ("A", "-"),
    ("E", "-"),
    # ("̄", "ː"), # TODO: Understand how to apply this to all long vowels
    ("y", "j"),
    ("ǯ", "g"),
    ("ǯ", "g"), # ǯ doesn't work, and dʒ is treated as two characters
    ("γ", "ɣ"),
    ("ḫ", "x"),
    ("ṯ̣", "θˤ"), # http://sed-online.ru/words/25279
    ("ṯ", "θ"),
    ("ṯ", "θ"),
    ("ˁ", "ʕ"),
    ("ˀ", "ʔ"),
    ("ˀ̣", "̣ʔ"),
    ("ā̆", "a"),  # long short vowel doesn't make sense
    ("āⁿ", "aː"), # We ignore tanween since unrelated to proto-semitic
    ("ā", "aː"),
    ("ă", "ă"),  # TODO: understand why this transcription is not automatically applied even though it is in the orthographic profile.
    ("ǟ", "æː"),
    ("ǟ", "æː"),
    ("ä", "æ"),  # 2 chars to 1
    ("ä", "æ"),
    ("aⁿ", "a"), # We ignore tanween since unrelated to proto-semitic
    ("ī̆", "i"),  # long short vowel doesn't make sense
    ("ī", "iː"),
    ("iⁿ", "iː"), # We ignore tanween since unrelated to proto-semitic
    ("ū̆", "u"),  # long short vowel doesn't make sense
    ("ū", "uː"),
    ("ō̆", "o"),  # long short vowel doesn't make sense
    ("ō", "oː"),
    ("ŏ", "ŏ"),
    ("ē̆", "e"),  # long short vowel doesn't make sense
    ("ē", "eː"),
    ("ә", "ə"),
    ("ṗ", "p"),
    ("ǧ", "g"),
    ("š", "ʃ"),
    ("ṣ̂", "ɬˤ"),
    ("ŝ", "ɬ"), # voiceless alveolar lateral fricative consonant
    ("ṣ̂", "ɬˤ"),
    # ("ŝₓ", "ɬ|s"), # TODO: implement uncertainty
    ("ľ", "l"), # )  # soqotri, uncertain
    ("ṣ", "sˤ"),  # ص
    # ("ḏ̣̣", "ðˤ"), # shouldn't be needed but the pipeline is not working properly
    ("ḏ", "ð"), # ذ
    ("ð̣", "ðˤ"), # ظ
    ("ḥ" ,"ħ"),  #ح
    ("ḳ", "qˤ"),  #ق
    ("ḵ" ,"k̠"),
    ("ġ", "ɣ"),  #غ
    ("ṭ", "tˤ"),  #ط
    # ("ẓ", "zˤ"),  #ظ
    ("ḍ", "dˤ"), #ض
    # ("ḍ", "d̪ˡ"),  # ض
    ("ẑ", "ɬ̬ˤ"), # https://en.wikipedia.org/wiki/Mehri_language
    ("ẑ", "ɬ̬ˤ"), # https://en.wikipedia.org/wiki/Mehri_language
    ("έ", "ɛ"), # https://en.wikipedia.org/wiki/Mehri_language
    ("έ", "ɛ"),
    ("έ", "ɛ"),
    ("’", ""), # ignore
    ("х", "x"),
    ("ﬁ", "fi"),
    ("ṓ", "oː"),
    ("ẹ́", "eː"),
    ("ẹ́", "eː"),
    # from emphatic interdental fricative to velarized voiced dental fricative
]