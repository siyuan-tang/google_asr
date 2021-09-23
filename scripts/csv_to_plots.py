import pandas as pd
import matplotlib.pyplot as plt


transcript_path = "/Users/tsy/Desktop/google/shilin/csv/test_nbest_test.csv"
output_path = "/Users/tsy/Desktop/google/shilin/csv/test_nbest_testresult.csv"

df = pd.read_csv(transcript_path)
lines=[]

threshold = 0.75
while 0.7 < threshold <= 1:

    # reject percentage
    reject = df[df['sentence_confidence'] < threshold].shape[0]
    rej_percents = reject / df.shape[0]

    accept = df[df['sentence_confidence'] > threshold]['wer'].to_list()

    # average accepted WER:
    if len(accept) != 0:
        acc_wer = sum(accept) / len(accept)

    # average overall WER
    ave_wer = sum(accept) / df.shape[0]

    # overall WER with human errors
    human_error = reject * 0.05
    human_wer = (sum(accept) + human_error) / df.shape[0]

    # overall cost
    cost = 0.1 * reject

    threshold += 0.02

    new_line = f"{threshold},{acc_wer},{ave_wer},{human_wer},{rej_percents},{cost}\n"

    lines.append(new_line)

with open(output_path, "w") as f:
    f.write("hreshold,acc_wer,ave_wer,human_wer,rej_percents,cost\n")
    f.writelines(lines)