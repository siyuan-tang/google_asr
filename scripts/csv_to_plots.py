import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("test_out.csv")
# plt.scatter(df['sentence_confidence'], df['wer'])
plt.scatter(df['min_word_confidence'], df['wer'])
plt.show()
