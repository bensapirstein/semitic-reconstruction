## Specification of form manipulation


Specification of the value-to-form processing in Lexibank datasets:

The value-to-form processing is divided into two steps, implemented as methods:
- `FormSpec.split`: Splits a string into individual form chunks.
- `FormSpec.clean`: Normalizes a form chunk.

These methods use the attributes of a `FormSpec` instance to configure their behaviour.

- `brackets`: `{'(': ')'}`
  Pairs of strings that should be recognized as brackets, specified as `dict` mapping opening string to closing string
- `separators`: `,/ `
  Iterable of single character tokens that should be recognized as word separator
- `missing_data`: `['∅']`
  Iterable of strings that are used to mark missing data
- `strip_inside_brackets`: `True`
  Flag signaling whether to strip content in brackets (**and** strip leading and trailing whitespace)
- `replacements`: `[('*', ''), ('\xad', ''), ('1', ''), ('V̄', '-'), ('V', '-'), ('̱V', '-'), ('S', '-'), ('ˇ', '-'), ('I', '-'), ('A', '-'), ('y', 'j'), ('ǯ', 'g'), ('ǯ', 'g'), ('γ', 'ɣ'), ('ḫ', 'x'), ('ṯ̣', 'θˤ'), ('ṯ', 'θ'), ('ṯ', 'θ'), ('ˁ', 'ʕ'), ('ˀ', 'ʔ'), ('ˀ̣', '̣ʔ'), ('ā̆', 'a'), ('āⁿ', 'aː'), ('ā', 'aː'), ('ă', 'ă'), ('ǟ', 'æː'), ('ǟ', 'æː'), ('ä', 'æ'), ('ä', 'æ'), ('aⁿ', 'a'), ('ī̆', 'i'), ('ī', 'iː'), ('iⁿ', 'iː'), ('ū̆', 'u'), ('ū', 'uː'), ('ō̆', 'o'), ('ō', 'oː'), ('ŏ', 'ŏ'), ('ē̆', 'e'), ('ē', 'eː'), ('ә', 'ə'), ('ṗ', 'p'), ('ǧ', 'g'), ('š', 'ʃ'), ('ṣ̂', 'ɬˤ'), ('ŝ', 'ɬ'), ('ṣ̂', 'ɬˤ'), ('ḏ', 'ð'), ('ð̣', 'ðˤ'), ('ḥ', 'ħ'), ('ḳ', 'qˤ'), ('ṣ', 'sˤ'), ('ṭ', 'tˤ'), ('ḍ', 'dˤ')]`
  List of pairs (`source`, `target`) used to replace occurrences of `source` in formswith `target` (before stripping content in brackets)
- `first_form_only`: `True`
  Flag signaling whether at most one form should be returned from `split` - effectively ignoring any spelling variants, etc.
- `normalize_whitespace`: `True`
  Flag signaling whether to normalize whitespace - stripping leading and trailing whitespace and collapsing multi-character whitespace to single spaces
- `normalize_unicode`: `None`
  UNICODE normalization form to use for input of `split` (`None`, 'NFD' or 'NFC')