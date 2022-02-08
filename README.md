# PyProfanity

A text-based profanity detector written in python, targeting the English language.

## Usage
```python
from profanity import contains_profanity

if contains_profanity("wow this fffrrricking works"):
    print("Nice.")
```

## About
The key to the success of this filter is a 5-stage algorithm with two passes, where on the second pass **lookalike unicode characters are replaced with their ascii equivalents**

Profanity filters, as with any kind of content filter, will always suffer to some extent from false positives, false negatives, or both.

This program errs on the side of having some false positives, but is better than most filters I've seen at minimizing them. False negatives are very uncommon with this filter. The only way to get them is to find undiscovered unicode lookalikes or to use a non-text based method, like sending multiple messages each with a letter of a swear word, or to send an image (since this filter only deals with text)

### Algorithm
1. Remove reserved _clean strings_. These are explictly enumerated in `profanity/profanity.json`, and you can add to them if you find a word or phrase that is picked up by the filter against your wishes.
2. Check for _priority profanity_. This is a way to dynamically add phrases or words that aren't in the profanity list by default, or are difficult to pick up.
3. Parse words as continuous strings of ascii letters (char codes 65-90 and 97-122). Example: `hel8lo, the.re` would be parsed as `["hel", "lo", "the", "re"]`.
4. Remove known clean english* words from the list, and concatenate all the remaining words back together. English words are sourced from `profanity/english_words.txt`, but that list does contain a few "non-english" words.
5. Check for profanity using char-patterns rather than exact string matches. So `hell` would look for any number of `h` followed by any number of `e`, etc. `hell` would be picked up in the string `hell`, `hheelllll`, `aheeell`, but not `hel`.
6. Repeat algorithm on original input string, but before stage 2 replace all unicode lookalikes with their ascii-letter equivalents.
7. Finally, return the union of the profanity detected in each pass.

Each step targets either reducing false positives or reducing false negatives.
1. reduce false +
2. reduce false -
3. reduce false -
4. reduce false +
5. reduce false -
6. reduce false -
