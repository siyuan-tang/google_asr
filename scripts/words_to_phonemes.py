
class PronunciationDict:

    words_to_phonemes = dict()

    def __init__(self, filename):
        self.words_to_phonemes = self.load_pron_dict(filename)

        # Beep has no entry for words like 'B' and 'C' - instead they appear as 'B.' and 'C.'
        # For these letter make 'B' by copying 'B.' and 'C' by copying 'C.' etc
        dotted_letters = "BCDFGHJKLMNPRSTUVYZ"
        for letter in dotted_letters:
            self.words_to_phonemes[letter] = self.words_to_phonemes[letter + "."]

        # Also beep has no entry for 0, 1, 2 etc - make these by copying the corresponding number
        numbers = [
            "zero",
            "one",
            "two",
            "three",
            "four",
            "five",
            "six",
            "seven",
            "eight",
            "nine",
        ]
        for i, itext in enumerate(numbers):
            self.words_to_phonemes[str(i)] = self.words_to_phonemes[itext.upper()]

    def load_pron_dict(self, filename):
        """Build a pronuncation dictionary from a file"""
        pron_dict = dict()
        with open(filename, "r") as f:
            for line in f:
                word = line.split()[0]
                phonemes = line.split()[1:]
                pron_dict[word] = phonemes
        return pron_dict


    def get_phonemes(self, sentence):
        """Convert sentence string into a list of phonemes"""
        words = sentence.split()
        # Make phonemes as a list of list (i.e separate list for each word)
        # for w in words:
        phonemes = []
        for w in words:
            try:
                phoneme = [self.words_to_phonemes[w.upper()]]
            except(KeyError):
                phoneme = [[w]]
            phonemes.append(phoneme)
        # Flatten into a single list
        phonemes = [phon for sublist in phonemes for item in sublist for phon in item]
        return phonemes
