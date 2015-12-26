"""

Mocks the NLTK corpus and should ONLY be used for testing because
the code is specifically tuned to what the tests query! Should the
tests change, be sure to check that this file is still compatible by
raising an ImportError in views.py when trying to import wordnet from
nltk.corpus. Then run the tests. Otherwise, make changes as necessary!

"""


def synsets(word):
    if word == "trollify":
        return None

    if word == "dog":
        return [
            Synset([
                "dog",
                "domestic_dog",
                "Canis_familiaris"
            ]),
            Synset([
                "dog",
                "frump"
            ]),
            Synset([
                "cad",
                "bounder"
            ]),
        ]


class Synset:
    def __init__(self, synonyms):
        self.synonyms = synonyms

    def lemma_names(self):
        return self.synonyms
