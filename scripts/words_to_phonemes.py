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
        phonemes = [self.words_to_phonemes[w.upper()] for w in words]
        # Flatten into a single list
        phonemes = [item for sublist in phonemes for item in sublist]
        return phonemes


def main():

    # Firt make a pronuncation dictionary object using the 'beep-1.0' file.
    # The file needs to be in the same directory as the python code.
    pron_dict = PronunciationDict("beep-1.0")

    # We can now use the dictionary to convert sentences into lists of phonemes.

    # Convert a sentence into phonemes
    sentence = "This is a sentence that we want to convert into a list of phonemes"
    phonemes = pron_dict.get_phonemes(sentence)
    print(sentence)
    print(phonemes)

    # Convert a word into phonemes
    word = "bin"
    phonemes = pron_dict.get_phonemes(word)
    print(word)
    print(phonemes)

    # Check that all the alphabet letters work
    sentence = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z"
    phonemes = pron_dict.get_phonemes(sentence)
    print("Letters")
    print(phonemes)

    # Check that all the numbers work
    sentence = "0 1 2 3 4 5 6 7 8 9"
    phonemes = pron_dict.get_phonemes(sentence)
    print("Numbers:")
    print(phonemes)

    # Check that it works for a grid like sentence
    sentence = "Bin blue at P 6 now"
    phonemes = pron_dict.get_phonemes(sentence)
    print(sentence)
    print(phonemes)


if __name__ == "__main__":
    main()
