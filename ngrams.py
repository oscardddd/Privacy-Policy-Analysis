import numpy as np
import pandas as pd
# import readability
from fuzzywuzzy import fuzz
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


nltk.download("punkt")
nltk.download('stopwords')
nlp = spacy.load("en_core_web_sm")
from nltk.corpus import stopwords
tparty_counts = {}
# entity_counts = {}
# regions = ['USA', 'England']
regulate_entity = ['NAI', 'DAA', 'EDAA', 'BBB', 'TrustArc']

third_parties = ['Google', 'Facebook','Twitter', 'Amazon', 'Yahoo', 'AOL']


track_list = ['Cookies', 'Web Beacons', 'Supercookies']
def collect(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        test_md = f.read()
        # test_md_clean = clean_md_bs4(test_md)
        test_md_clean_bs4 = clean_md(test_md)

        return test_md_clean_bs4

def top_entity(region):
    print("Start working on region: ", region, '\n')
    # textlist = ''
    folder_path = './final'
    i = 1
    entity_counts = Counter()

    for filename in os.listdir(f'{folder_path}/{region}'):
        nlp.max_length = 2000000
        if filename.endswith(".md"):  # Check if the file is a markdown file
            print(i)
            i += 1
            file_path = os.path.join(f'{folder_path}/{region}', filename)
            text = collect(file_path)
            doc = nlp(text)
            for ent in doc.ents:
                entity_counts[ent.text] += 1




def biggygram(n):

    folder_path = './final/'
    i = 1
    res = []
    for subfolder in os.listdir(folder_path):
        region = subfolder[:2]
        print("working on region rn: ", region)
        big_ngram = []

        for filename in os.listdir(f'./final/{subfolder}'):
            # print(filename)
            if filename.endswith(".md"):  # Check if the file is a markdown file
                file_path = os.path.join(f'./final/{subfolder}', filename)
                text = collect(file_path)
                big_ngram = big_ngram + n_gram(n, text)
                print(i)
                i += 1

        res = res + big_ngram
    # print(res)

    bigram_freq = Counter(res)

    sorted_bigrams = sorted(bigram_freq.items(), key=lambda x: x[1], reverse=True)

    print(sorted_bigrams [:5])


def bigngram(n):
    if n == 4:
        folder_path = './final/'
        i = 1
        for subfolder in os.listdir(folder_path):
            region = subfolder[:2]
            print(region)
            big_ngram = []

            for filename in os.listdir(f'./final/{subfolder}'):
                # print(filename)
                if filename.endswith(".md"):  # Check if the file is a markdown file
                    file_path = os.path.join(f'./final/{subfolder}', filename)
                    text = collect(file_path)
                    big_ngram = big_ngram + n_gram(n, text)
                    print(i)
                    i += 1

            bigram_freq = Counter(big_ngram)

            sorted_bigrams = sorted(bigram_freq.items(), key=lambda x: x[1], reverse=True)


            # df = pd.DataFrame(sorted_bigrams, columns=['Bigram', 'Frequency'])
            # df['Bigram'] = df['Bigram'].apply(lambda x: ' '.join(x))  # Convert bigram tuples to strings
            # plt.figure(figsize=(19, 8))
            # sns_plot = sns.barplot(x='Frequency', y='Bigram', data=df.head(20))  # Adjust the number to display as needed
            # plt.title('Top 20 4grams')
            # plt.xlabel('Frequency')
            # plt.ylabel('4grams')
            # plt.xlim(0, 1000)
            # ax = sns_plot.axes
            # for p in ax.patches:
            #     ax.annotate(f'{int(p.get_width())}',
            #                 (p.get_width(), p.get_y() + p.get_height() / 2.),
            #                 ha = 'left', va = 'center',
            #                 xytext = (5, 0),
            #                 textcoords = 'offset points')
            #
            # plot_save_path = os.path.join(f'./graphs/4grams', f'4gram_plot_{region}.png')
            # # plt.show()
            # plt.savefig(plot_save_path)
            # plt.close()

    elif n == 3:
        folder_path = './final/'
        i = 1
        for subfolder in os.listdir(folder_path):
            region = subfolder[:2]
            print(region)
            big_ngram = []

            for filename in os.listdir(f'./final/{subfolder}'):
                # print(filename)
                if filename.endswith(".md"):  # Check if the file is a markdown file
                    file_path = os.path.join(f'./final/{subfolder}', filename)
                    text = collect(file_path)
                    big_ngram = big_ngram + n_gram(n, text)
                    print(i)
                    i += 1

            bigram_freq = Counter(big_ngram)

            sorted_bigrams = sorted(bigram_freq.items(), key=lambda x: x[1], reverse=True)
            df = pd.DataFrame(sorted_bigrams, columns=['Bigram', 'Frequency'])
            df['Bigram'] = df['Bigram'].apply(lambda x: ' '.join(x))  # Convert bigram tuples to strings
            plt.figure(figsize=(18, 8))
            sns_plot = sns.barplot(x='Frequency', y='Bigram',
                                   data=df.head(20))  # Adjust the number to display as needed
            plt.title('Top 20 4grams')
            plt.xlabel('Frequency')
            plt.ylabel('trigrams')
            plt.xlim(0, 4000)
            ax = sns_plot.axes
            for p in ax.patches:
                ax.annotate(f'{int(p.get_width())}',
                            (p.get_width(), p.get_y() + p.get_height() / 2.),
                            ha='left', va='center',
                            xytext=(5, 0),
                            textcoords='offset points')

            plot_save_path = os.path.join(f'./graphs/trigrams', f'trigram_plot_{region}.png')
            # plt.show()
            plt.savefig(plot_save_path)
            plt.close()


    elif n == 5:
        folder_path = './final/'
        i = 1
        for subfolder in os.listdir(folder_path):
            region = subfolder[:2]
            print(region)
            big_ngram = []

            for filename in os.listdir(f'./final/{subfolder}'):
                # print(filename)
                if filename.endswith(".md"):  # Check if the file is a markdown file
                    file_path = os.path.join(f'./final/{subfolder}', filename)
                    text = collect(file_path)
                    big_ngram = big_ngram + n_gram(n, text)
                    print(i)
                    i += 1

            bigram_freq = Counter(big_ngram)

            sorted_bigrams = sorted(bigram_freq.items(), key=lambda x: x[1], reverse=True)
            df = pd.DataFrame(sorted_bigrams, columns=['Bigram', 'Frequency'])
            df['Bigram'] = df['Bigram'].apply(lambda x: ' '.join(x))  # Convert bigram tuples to strings
            plt.figure(figsize=(18, 8))
            sns_plot = sns.barplot(x='Frequency', y='Bigram',
                                   data=df.head(20))  # Adjust the number to display as needed
            plt.title('Top 20 4grams')
            plt.xlabel('Frequency')
            plt.ylabel('5grams')
            plt.xlim(0, 800)
            ax = sns_plot.axes
            for p in ax.patches:
                ax.annotate(f'{int(p.get_width())}',
                            (p.get_width(), p.get_y() + p.get_height() / 2.),
                            ha='left', va='center',
                            xytext=(5, 0),
                            textcoords='offset points')

            plot_save_path = os.path.join(f'./graphs/5grams', f'5ram_plot_{region}.png')
            # plt.show()
            plt.savefig(plot_save_path)
            plt.close()

def n_gram(n, text):
    phrase_gens = []
    stop_words = set(stopwords.words('english'))
    word_list = nltk.word_tokenize(text)
    # print(len(word_list))
    word_list = list(filter(lambda w: any((c.isalpha() for c in w)), word_list))
    # word_list = list(filter(lambda w: w not in stop_words, word_list))
    word_list = list(filter(lambda w: w not in string.punctuation, word_list))

    # print(len(word_list))

    bigrams = list(nltk.ngrams(word_list, n, pad_left=False, pad_right=False ))
    return bigrams

def movedata():

    for filename in os.listdir('./brge'):
        if filename.endswith('.md'):
            code = filename[:2]
            if not os.path.exists(f'./final2/{code}'):
                os.makedirs(f'./final2/{code}')
                print(f"Directory f'./final2/{code}' was created.")
            else:
                print(f"Directory f'/final2/{code}' already exists.")

            shutil.move(f'./brge/{filename}', f'./final2/{code}')



def makdir():
    regions = ['al', 'au', 'at', 'be', 'br', 'bg', 'ca', 'co', \
               'hr', 'cz', 'dk', 'ee', 'fi', 'fr', 'de', 'gr', \
               'hk', 'hu', 'ie', 'il', 'it', 'jp', 'lv', 'mx', \
               'nl', 'nz', 'no', 'pl', 'pt', 'ro', 'rs', 'sg', \
               'sk', 'za', 'es', 'se', 'ch', 'gb', 'ua', 'us']

    for code in regions:
        if not os.path.exists(f'./final/{code}'):
            os.makedirs(f'./final/{code}')
            print(f"Directory f'./final/{code}' was created.")
        else:
            print(f"Directory f'/final/{code}' already exists.")

# output the result for the third-party case
def third_party_result():
    entity_counts = {}
    regions = []
    entities = []
    counts = []

    for filename in os.listdir('./thirdparty'):
        region = filename[:2]
        with open(f'./thirdparty/{filename}', 'r', encoding='utf-8') as f:
            data = json.load(f)
            for key in data:
                regions.append(region)
                entities.append(key)
                counts.append(data[key])

    df = pd.DataFrame({
        'Region': regions,
        'Entity': entities,
        'Count': counts
    })

    # plt.figure(figsize=(10, 6))
    # sns.lineplot(data=df, x='Region', y='Count', hue='Entity', marker='o', sort=False)
    # lines = plt.gca().get_lines()
    # for line in lines:
    #     line.set_linestyle(':')
    # plt.title('Entity Counts Across Different Regions')
    # plt.xlabel('Region')
    # plt.ylabel('Count')
    # plt.legend(title='Entity')
    # plt.grid(True)
    # plt.show()

    plt.figure(figsize=(12, 6))
    sns.barplot(data=df, x='Region', y='Count', hue='Entity', dodge=True)  # dodge=True creates grouped bars

    plt.title('Third-Party Entity Counts Across Different Regions')
    plt.xlabel('Region')
    plt.ylabel('Count')
    plt.legend(title='Entity')
    plt.xticks(rotation=45)  # Rotate the region names for better readability
    plt.show()


def third_party_all():
    for region in os.listdir('./final'):
        # print("Now processing ", region, '\n')

        third_party_ner(region)


# Track the third-party entity for each region individually
def third_party_ner(region):
    print("Start working on region: ", region, '\n')
    entity_counts = {'Google':0, 'Facebook':0, 'Twitter':0, 'Amazon':0, 'Yahoo':0, 'AOL':0}
    # textlist = ''
    folder_path = './final'
    i = 1
    for filename in os.listdir(f'{folder_path}/{region}'):
        nlp.max_length = 2000000
        if filename.endswith(".md"):  # Check if the file is a markdown file
            print(i)
            i += 1
            file_path = os.path.join(f'{folder_path}/{region}', filename)
            text = collect(file_path)
            doc = nlp(text)

            for ent in doc.ents:
                for entity_word in third_parties:
                    pattern = re.compile(re.escape(entity_word), re.IGNORECASE)
                    if pattern.search(ent.text):
                        entity_counts[entity_word] += 1

    output_path = os.path.join('./thirdparty', f"{region}_counts.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(entity_counts, f, ensure_ascii=False, indent=4)

def tracking_result():
    entity_counts = {}
    regions = []
    entities = []
    counts = []

    for filename in os.listdir('./tracking_tech'):
        region = filename[:2]
        with open(f'./tracking_tech/{filename}', 'r', encoding='utf-8') as f:
            data = json.load(f)
            for key in data:
                regions.append(region)
                entities.append(key)
                counts.append(data[key])

    df = pd.DataFrame({
        'Region': regions,
        'Entity': entities,
        'Count': counts
    })
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df, x='Region', y='Count', hue='Entity', dodge=True)  # dodge=True creates grouped bars

    plt.title('Tracking Technology Counts Across Different Regions')
    plt.xlabel('Region')
    plt.ylabel('Count')
    plt.legend(title='Entity')
    plt.xticks(rotation=45)  # Rotate the region names for better readability
    plt.show()

def tracking_all():
    for region in os.listdir('./final'):
        tracking_ner(region)


def tracking_ner(region):
    print("Start working on region: ", region, '\n')
    tracking_counts = {'Cookies':0, 'Web Beacons':0, 'Supercookies':0}
    folder_path = './final'
    i = 1
    for filename in os.listdir(f'{folder_path}/{region}'):
        nlp.max_length = 2000000
        if filename.endswith(".md"):  # Check if the file is a markdown file
            print(i)
            i += 1
            file_path = os.path.join(f'{folder_path}/{region}', filename)
            text = collect(file_path)
            doc = nlp(text)

            for ent in doc.ents:
                for entity_word in track_list:
                    pattern = re.compile(re.escape(entity_word), re.IGNORECASE)
                    if pattern.search(ent.text):
                       tracking_counts[entity_word] += 1

    output_path = os.path.join('./tracking_tech', f"{region}_counts.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(tracking_counts, f, ensure_ascii=False, indent=4)


def regulations_result():
    entity_counts = {}
    regions = []
    entities = []
    counts = []

    for filename in os.listdir('./regulations'):
        region = filename[:2]
        with open(f'./regulations/{filename}', 'r', encoding='utf-8') as f:
            data = json.load(f)
            for key in data:
                regions.append(region)
                entities.append(key)
                counts.append(data[key])

    df = pd.DataFrame({
        'Region': regions,
        'Entity': entities,
        'Count': counts
    })
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df, x='Region', y='Count', hue='Entity', dodge=True)  # dodge=True creates grouped bars

    plt.title('Regulation Entity Counts Across Different Regions')
    plt.xlabel('Region')
    plt.ylabel('Count')
    plt.legend(title='Entity')
    plt.xticks(rotation=45)  # Rotate the region names for better readability
    plt.show()

def regulation_all():
    for region in os.listdir('./final'):
        regulation_ner(region)
def regulation_ner(region):
    print("Start working on region: ", region, '\n')
    regulate_entity = ['NAI', 'DAA', 'EDAA', 'BBB', 'TrustArc']
    regulate_counts = {}
    for key in regulate_entity:
        regulate_counts[key] = 0

    folder_path = './final'
    i = 1
    for filename in os.listdir(f'{folder_path}/{region}'):
        nlp.max_length = 2000000
        if filename.endswith(".md"):  # Check if the file is a markdown file
            print(i)
            i += 1
            file_path = os.path.join(f'{folder_path}/{region}', filename)
            text = collect(file_path)
            doc = nlp(text)

            for ent in doc.ents:
                for entity_word in regulate_entity:
                    pattern = re.compile(re.escape(entity_word), re.IGNORECASE)
                    if pattern.search(ent.text):
                       regulate_counts[entity_word] += 1

    output_path = os.path.join('./regulations', f"{region}_counts.json")

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(regulate_counts, f, ensure_ascii=False, indent=4)

#打印出一个国家最多的entity frequency
def simple_ner():
    entlist = []
    textlist = ''
    folder_path = './test'
    for filename in os.listdir(folder_path):
        if filename.endswith(".md"):  # Check if the file is a markdown file
            file_path = os.path.join(folder_path, filename)
            text = collect(file_path)
            textlist = textlist + '\n' + text
    doc = nlp(textlist)

    for ent in doc.ents:
        entlist.append(ent.text)
    # print(entlist)
    ent_freq = Counter(entlist)
    # print(ent_freq)

    sorted_ent= sorted(ent_freq.items(), key=lambda x: x[1], reverse=True)

    df = pd.DataFrame(sorted_ent, columns=['Entity name', 'Frequency'])
    df['Entity name'] = df['Entity name'].apply(lambda x: ' '.join(x))  # Convert bigram tuples to strings
    plt.figure(figsize=(12, 8))
    sns.barplot(x='Frequency', y='Entity name', data=df.head(20))  # Adjust the number to display as needed
    plt.title('Top 20 Entities')
    plt.xlabel('Frequency')
    plt.ylabel('Entities')
    plt.show()

def ner_graph():
    entity_counts = {}
    regions = []
    entities = []
    counts = []

    # Iterate over the dictionary to populate the lists
    for region, entities_counts in entity_counts.items():
        for entity, count in entities_counts.items():
            regions.append(region)
            entities.append(entity)
            counts.append(count)

    print(entity_counts)
    df = pd.DataFrame({
        'Region': regions,
        'Entity': entities,
        'Count': counts
    })

    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x='Region', y='Count', hue='Entity', marker='o', sort=False)
    plt.title('Entity Counts Across Different Regions')
    plt.xlabel('Region')
    plt.ylabel('Count')
    plt.legend(title='Entity')
    plt.grid(True)
    plt.show()



if __name__=="__main__":
    movedata()
    # third_party_result()
    # bigngram(5)
    # bigngram(2)
    # third_party_all()
    # third_party_ner('aha')
    # movedata()
    # third_party_ner('au')
    # tracking_all()
    # regulation_all()
    # tracking_result()
    # regulations_result()
    # biggygram(5)