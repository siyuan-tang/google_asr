import pandas as pd


transcript_path = "/Users/tsy/Desktop/google/google_asr/csv/adaptation/gender/test_female.csv"
output_path = "/Users/tsy/Desktop/google/google_asr/csv/adaptation/gender/test_result_female.csv"

df = pd.read_csv(transcript_path)
lines=[]

threshold = 0.75
while 0.7 < threshold <= 1:

    # reject percentage
    reject = df[df['sentence_confidence'] < threshold].shape[0]
    rej_percents = reject / df.shape[0]

    accept = df[df['sentence_confidence'] > threshold]['wer'].to_list()
    accept_p = df[df['sentence_confidence'] > threshold]['per'].to_list()

    # average accepted WER:
    if len(accept) != 0:
        acc_wer = sum(accept) / len(accept)

    if len(accept_p) != 0:
        acc_per = sum(accept_p) / len(accept_p)

    # average overall WER
    ave_wer = sum(accept) / df.shape[0]
    ave_per = sum(accept_p) / df.shape[0]

    # overall WER with human errors
    human_error = reject * 0.05
    human_wer = (sum(accept) + human_error) / df.shape[0]
    human_per = (sum(accept_p) + human_error) / df.shape[0]

    # overall cost
    cost = 0.1 * reject

    threshold += 0.001

    new_line = f"{threshold},{ave_wer},{ave_per},{human_wer},{human_per},{rej_percents}\n"

    # {acc_wer},{acc_per},{cost}

    lines.append(new_line)

with open(output_path, "w") as f:
    f.write("threshold,ave_wer,ave_per,human_wer,human_per,rej_percents\n")
    f.writelines(lines)