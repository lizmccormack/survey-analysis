# -*- coding: utf-8 -*-

import string
import nltk
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

"""
This script uses NLP tools to analyze text based on specific inputs from the user
in the following steps:
1. Find word frequency of all words in text, and outputs them in a table and bar
graph

input: CSV file with a column name as first row
output: bar graph and data frame with words and word count

2.user entered exploratory key words to analyze specific word frequency and produce word
frequency graph, word cloud, polarity and subjectivity, and output results in csv file.

input: user words
output: bar graph, wordcloud, csv with word frequency, and polarity/subjectivity values
"""

# read text data CSV
df = pd.read_csv('text_data.csv', sep=',', nrows=14000, encoding='latin-1')

# find word frequency
top_N = 10
txt = df.Response.str.lower().str.replace(r'\|', ' ').str.cat(sep=' ')
words = nltk.tokenize.word_tokenize(txt)
word_dist = nltk.FreqDist(words)

stopwords = nltk.corpus.stopwords.words('english')
words_except_stop_dist = nltk.FreqDist(w for w in words if w not in stopwords)

print('All frequencies, excluding STOPWORDS:')
print('=' * 100)
rslt = pd.DataFrame(words_except_stop_dist.most_common(top_N),
                    columns=['Word', 'Frequency'])
print(rslt)
print('=' * 100)

writer = pd.ExcelWriter('environment_wordcascade_2.xlsx', engine='xlsxwriter')
rslt.to_excel(writer, sheet_name='Sheet1')
writer.save()

rslt.plot.bar(x="Word", y="Frequency",rot=0)
plt.xticks(rotation=90)
plt.show()

# user inputs words
print ("Hello, Let's analyze some survey responses!")
word_1=input("Enter first word:")
word_2=input("Enter second word:")
word_3=input("Enter third word:")

#calculate frequency of words
def calculate_word(Response):
    blob = TextBlob(Response)
    return blob.word_counts[word_1]

df[word_1] = df.Response.apply(calculate_word)

def calculate_word(Response):
    blob = TextBlob(Response)
    return blob.word_counts[word_2]

df[word_2] = df.Response.apply(calculate_word)

def calculate_word(Response):
    blob = TextBlob(Response)
    return blob.word_counts[word_3]

df[word_3] = df.Response.apply(calculate_word)

#sum words frequnecy
word_1_total = df[word_1].sum()
word_2_total = df[word_2].sum()
word_3_total = df[word_3].sum()

#create new row with sums
df.loc['total'] = df.select_dtypes(pd.np.number).sum()

# manipulate dataframe
df_2 = df.transpose()
df_3 = df_2.iloc[1:]
word = [word_1, word_2, word_3]
df_3['word'] = word

# create bar graph
df_3.plot.bar(x="word", y="total", rot=0)
plt.show()

comment_words = ' '
stopwords = set(STOPWORDS)

for val in df.Response:
    val = str(val)
    tokens = val.split()
    for i in range(len(tokens)):
        tokens[i] = tokens[i].lower()
    for words in tokens:
        comment_words = comment_words + words + ' '

wordcloud = WordCloud(width = 800, height = 800,
                background_color ='white',
                stopwords = stopwords,
                min_font_size = 10).generate(comment_words)

# plot the WordCloud image
plt.figure(figsize = (8, 8), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)

plt.show()

# calculate sentiment and polarity
def calculate_polarity(Response):
    blob = TextBlob(str(Response))
    polarity = blob.sentiment.polarity
    return polarity

def calculate_subjectivity(Response):
    blob = TextBlob(str(Response))
    subjectivity = blob.sentiment.subjectivity
    return subjectivity

def calculate_polarity_adj(Response):
    blob = TextBlob(str(Response))
    if blob.sentiment.polarity > 0:
        return 'positive'
    elif blob.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

def calculate_subjectivity_adj(Response):
    blob = TextBlob(str(Response))
    if blob.sentiment.subjectivity < 0.5:
        return 'objective'
    else:
        return 'subjective'

df['polarity'] = df.Response.apply(calculate_polarity)
df['subjectivity'] = df.Response.apply(calculate_subjectivity)
df['polarity_adj'] = df.Response.apply(calculate_polarity_adj)
df['subjectivity_adj'] = df.Response.apply(calculate_subjectivity_adj)

# export dataframe to CSV file
df.to_csv('output.csv', sep=',', encoding='utf-8')
