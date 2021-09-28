import json
import glob
import os
import re
import jiwer
from ground_truth import filename_to_sentence
from words_to_phonemes import PronunciationDict

transcript_path = "/Users/tsy/Desktop/google/google_asr/data/adaptation/female/*/*.json"
output_path = "/Users/tsy/Desktop/google/google_asr/csv/adaptation/gender/test_female.csv"
pron_dict = PronunciationDict("beep-1.0")

def clean_hyp(hyp):
    """
    add space before and after numbers
    """
    new_hyp = []
    for token in hyp.split(" "):
        if re.findall(r"\d", token):
            # print(f"{token} has number")
            new_token = ""
            for letter in token:
                if letter.isnumeric():
                    new_token += f" {letter} "
                else:
                    new_token += letter
            # print(f"convert to: {new_token}")
            new_hyp.append(new_token)
        else:
            new_hyp.append(token)
            # print(f"{token} doesn't have number")

    return " ".join(new_hyp)


def get_wer(ground_truth, hypothesis):
    transformation = jiwer.Compose([
        jiwer.ToLowerCase(),
        jiwer.RemoveMultipleSpaces(),
        jiwer.RemovePunctuation(),
        jiwer.SentencesToListOfWords(word_delimiter=" ")
    ])

    wer = jiwer.wer(
        ground_truth,
        hypothesis,
        truth_transform=transformation,
        hypothesis_transform=transformation
    )

    return wer


lines = []
for json_file in glob.iglob(transcript_path, recursive=True):
    audio_name = json_file.split("/")[-1][:-5]
    spk_name = json_file.split("/")[-2]
    ground_truth = filename_to_sentence(audio_name)
    # print(json_file)

    # Load back from a file
    with open(json_file, 'r') as f:
        obj=json.load(f)

    # choose one-best transcript
    transcript = obj["results"][0]["alternatives"][0]["transcript"]
    asr_result = obj["results"][0]["alternatives"][0]
    sentence_confidence = asr_result["confidence"]
    word_confidences = []
    for word in asr_result['words']:
        word_confidences.append(word["confidence"])
    min_word_confidence = min(word_confidences)

    # choose highest confidence from n-best transcript
    # alts = []
    # for alt in obj["results"][0]["alternatives"]:
    #     text = alt["transcript"]
    #     conf = alt["confidence"]
    #     alts.append((text, conf))
    # sorted_alts = sorted(alts, reverse=True, key=lambda x: x[1])
    # highest_conf = sorted_alts[0]
    # transcript = highest_conf[0]
    # sentence_confidence = highest_conf[1]
    # min_word_confidence = "u"

    # get wer
    clean_transcript = clean_hyp(transcript)
    wer= get_wer(ground_truth, clean_transcript)

    # get phonemes error rate
    phonemes_truth = pron_dict.get_phonemes(ground_truth)
    phonemes_transcript = pron_dict.get_phonemes(clean_transcript)
    per = get_wer(phonemes_truth, phonemes_transcript)

    new_line = f"{spk_name},{audio_name},{sentence_confidence},{min_word_confidence},{wer},{per}\n"

    lines.append(new_line)

with open(output_path, "w") as f:
    f.write("speaker,filename,sentence_confidence,min_word_confidence,wer,per\n")
    f.writelines(lines)
