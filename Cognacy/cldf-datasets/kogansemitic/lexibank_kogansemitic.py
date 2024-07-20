import pathlib
import attr
from clldutils.misc import slug
from pylexibank import Dataset as BaseDataset
from pylexibank import progressbar as pb
from pylexibank import Language
from pylexibank import FormSpec

@attr.s
class CustomLanguage(Language):
    NameInSource = attr.ib(default=None)

class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "kogansemitic"
    form_spec = FormSpec(separators=",/ ", missing_data=["∅"], first_form_only=True,
                         replacements=[("*", ""),
                                       ("­", ""),
                                       ("1", ""),
                                       ("V̄", "-"),
                                       ("V", "-"),  # TODO: Implement Uncertainty (List 2023 4.2)
                                       ("̱V", "-"),
                                       ("S", "-"),
                                       # ("S", "s/š/ŝ"), # TODO: Implement Uncertainty (List 2023 4.2)
                                       ("ˇ", "-"),
                                       ("I", "-"),
                                       ("A", "-"),
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
                                       # ("ḏ̣̣", "ðˤ"), # shouldn't be needed but the pipeline is not working properly
                                       ("ḏ", "ð"), # ذ
                                       ("ð̣", "ðˤ"), # ظ
                                       ("ḥ" ,"ħ"),  #ح
                                       ("ḳ", "qˤ"),  #ق
                                       ("ṣ", "sˤ"),  #ص
                                       ("ṭ", "tˤ"),  #ط
                                       # ("ẓ", "zˤ"),  #ظ
                                       ("ḍ", "dˤ") #ض
                                       # ("ḍ", "d̪ˡ"),  # ض

                                       # from emphatic interdental fricative to velarized voiced dental fricative
                                       ])
    language_class = CustomLanguage

    # def cldf_specs(self):  # A dataset must declare all CLDF sets it creates.
    #     from cldfbench import CLDFSpec
    #     return CLDFSpec(dir=self.cldf_dir, module='StructureDataset')

    def cmd_download(self, args):
        """
        Download files to the raw/ directory. You can use helpers methods of `self.raw_dir`, e.g.
        """
        self.raw_dir.write("sed.tsv", self.dir.parent.parent.joinpath("sed.tsv").read_text())

    def cmd_makecldf(self, args):
        """
        Convert the raw data to a CLDF dataset.
        """
        # add bib
        args.writer.add_sources()
        args.log.info("added sources")

        concepts = {}
        for concept in self.concepts:
            idx = concept["NUMBER"]+"_"+slug(concept["ENGLISH"])
            concepts[concept["ENGLISH"]] = idx
            try:
                args.writer.add_concept(
                        ID=idx,
                        Name=concept["ENGLISH"],
                        Concepticon_ID=concept["CONCEPTICON_ID"],
                        Concepticon_Gloss=concept["CONCEPTICON_GLOSS"]
                        )
            except KeyError:
                args.writer.add_concept(
                        ID=idx,
                        Name=concept["ENGLISH"]
                        )

        languages = args.writer.add_languages(lookup_factory="Name")

        # read in data
        data = self.raw_dir.read_csv(
            "sed.tsv", delimiter="\t",
            dicts=True
        )
        # add data
        for i, row in pb(enumerate(data), desc="cldfify", total=len(data)):
            cog = row["COGID"]
            concept = row["CONCEPT"]
            # fetch cid from concepts if it exists
            cid = concepts.get(concept, None)
            if not cid:
                args.log.info(f"Concept for {row['ID']} not found")
                continue
            lid = slug(row["DOCULECT"])
            entry = row["VALUE"]
            for lex in args.writer.add_forms_from_value(
                    Language_ID=lid,
                    Parameter_ID=cid,
                    Value=entry,
                    Cognacy=cog
                # TODO: pass Source (conclude from notes)
                    ):
                args.writer.add_cognate(
                        lexeme=lex,
                        Cognateset_ID=cog
                        )
