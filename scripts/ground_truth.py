def filename_to_sentence(filename):
    # filename[0]
    if filename[0] == "b":
        first_word = "bin"
    elif filename[0] == "l":
        first_word = "lay"
    elif filename[0] == "p":
        first_word = "place"
    else:
        first_word = "set"

    # filename[1]
    if filename[1] == "b":
        second_word = "blue"
    elif filename[1] == "g":
        second_word = "green"
    elif filename[1] == "r":
        second_word = "red"
    else:
        second_word = "white"

    # filename[2]
    if filename[2] == "b":
        third_word = "by"
    elif filename[2] == "a":
        third_word = "at"
    elif filename[2] == "i":
        third_word = "in"
    else:
        third_word = "with"

    # filename[3]
    forth_word = filename[3]

    # filename[4]
    if filename[4] == "z":
        fifth_word = "0"
    else:
        fifth_word = filename[4]

    # filename[5]
    if filename[5] == "n":
        sixth_word = "now"
    elif filename[5] == "a":
        sixth_word = "again"
    elif filename[5] == "p":
        sixth_word = "please"
    else:
        sixth_word = "soon"

    sentence = first_word + " " + second_word + " " + third_word + " " + forth_word + " " + fifth_word + " " + sixth_word
    return sentence


# ground_truth = filename_to_sentence("bbay3n.wav.json")
# print(ground_truth)

# import os

# directory = r"./data/s12"

# for filename in os.listdir(directory):
#     ground_truth = filename_to_sentence(filename)
    # print(ground_truth)
#