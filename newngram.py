import nltk
from markdown_to_text import clean_md, clean_md_bs4
from collections import Counter
import spacy
import re
import string
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os
import json
import shutil
from ngrams import collect

nltk.download("punkt")
nltk.download('stopwords')
nlp = spacy.load("en_core_web_sm")
from nltk.corpus import stopwords
def test():
    word = "T"
    if re.search(r'tab', word, re.IGNORECASE):
        print("md")

# ngram for all
def ngram_all(n, topk):
    alllist = []
    with open('./nltk_results/nltk_truncated.json', 'r', encoding='utf-8') as json_file:
        entities = json.load(json_file)
        stop_words = set(stopwords.words('english'))

    for region in entities.keys():
        biglist = entities[region]

        print("Get all tokens! \n")

        word_list = list(filter(lambda w: any((c.isalpha() for c in w)), biglist))
        word_list = list(filter(lambda w: w not in stop_words, word_list))
        word_list = list(filter(lambda w: not re.search(r'tab', w, re.IGNORECASE), word_list))
        word_list = list(filter(lambda w: w not in string.punctuation, word_list))

        print("Finish all filterings! \n")

        alllist = alllist+word_list

    bigrams = list(nltk.ngrams(alllist, n, pad_left=False, pad_right=False))
    bigram_freq = Counter(bigrams)
    sorted_bigrams = sorted(bigram_freq.items(), key=lambda x: x[1], reverse=True)
    print("Get all sorted")
    df = pd.DataFrame(sorted_bigrams, columns=['Bigram', 'Frequency'])
    print(df.head(topk))
def newngram(n):
    entities = {}
    with open('./nltk_results/nltk_truncated.json', 'r', encoding='utf-8') as json_file:
        entities = json.load(json_file)
        stop_words = set(stopwords.words('english'))

    for region in entities.keys():
        biglist = entities[region]

        print("Get all tokens! \n")

        word_list = list(filter(lambda w: any((c.isalpha() for c in w)), biglist))
        word_list = list(filter(lambda w: w not in stop_words, word_list))
        word_list = list(filter(lambda w: not re.search(r'tab', w, re.IGNORECASE), word_list))
        word_list = list(filter(lambda w: w not in string.punctuation, word_list))

        print("Finish all filterings! \n")

        bigrams = list(nltk.ngrams(word_list, n, pad_left=False, pad_right=False ))
        bigram_freq = Counter(bigrams)
        sorted_bigrams = sorted(bigram_freq.items(), key=lambda x: x[1], reverse=True)

        print("Get all sorted")

        df = pd.DataFrame(sorted_bigrams, columns=['Bigram', 'Frequency'])
        df['Bigram'] = df['Bigram'].apply(lambda x: ' '.join(x))  # Convert bigram tuples to strings
        plt.figure(figsize=(20, 14))
        sns_plot = sns.barplot(x='Frequency', y='Bigram', data=df.head(10))  # Adjust the number to display as needed
        plt.title(f'Top 20 {n}grams {region}')
        plt.xlabel('Frequency')
        plt.ylabel(f'{n}grams')
        plt.xlim(0, 3000)
        ax = sns_plot.axes
        for p in ax.patches:
            ax.annotate(f'{int(p.get_width())}',
                        (p.get_width(), p.get_y() + p.get_height() / 2.),
                        ha = 'left', va = 'center',
                        xytext = (5, 0),
                        textcoords = 'offset points')

        plot_save_path = os.path.join(f'./graphs/truncated{n}gram/', f'20{region}.png')
        # plt.show()
        plt.savefig(plot_save_path)
        plt.close()

# Tokenize all documents and store into json file
def nltk_store():
    json_file_path = os.path.join('./nltk_results', "nltk_truncated.json")
    obj = {}
    # Save the entities to a JSON file
    for region in os.listdir('./final3'):
        l = direct_find(region)
        obj[region] = l

    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(obj, json_file, ensure_ascii=False, indent=4)

def direct_find(region):
    i = 1
    folder_path = './final3'

    bigwords = []
    print(f"processing {region}")
    for filename in os.listdir(f'{folder_path}/{region}'):
        if filename.endswith(".md"):  # Check if the file is a markdown file
            print(i)
            i += 1
            file_path = os.path.join(f'{folder_path}/{region}', filename)
            text = collect(file_path)
            wordlist = nltk.word_tokenize(text)
            bigwords = bigwords + wordlist

    return bigwords
if __name__=="__main__":
    # nltk_store()
    # newngram(4)
   # test()
   ngram_all(3, 10)