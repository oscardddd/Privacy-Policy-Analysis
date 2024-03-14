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


def regulations():
    regions = []
    entitylist = []
    counts = []
    third_parties = ['NAI', 'DAA', 'EDAA', 'BBB', 'TrustArc']
    pattern_dict = {entity_word: re.compile(re.escape(entity_word), re.IGNORECASE) for entity_word in third_parties}

    # for entity_word in third_parties:
    #     pattern = re.compile(re.escape(entity_word), re.IGNORECASE)
    i = 0
    with open('./nltk_results/nltk_results3.json', 'r', encoding='utf-8') as json_file:
        entities = json.load(json_file)
        print("successfully load file")
        # compile the re patttern for the six third parties
        for region in entities.keys():
            print(f"start on region {region}")
            entity_counts = {'NAI': 0, 'DAA': 0, 'EDAA': 0, 'BBB': 0, 'TrustArc': 0}
            for name in entities[region]:
                # print(name)
                for entity_word, pattern in pattern_dict.items():
                    if pattern.search(name):
                        entity_counts[entity_word] += 1

            for i in entity_counts.keys():
                regions.append(region)
                entitylist.append(i)
                counts.append(entity_counts[i])

    df = pd.DataFrame({
        'Region': regions,
        'Entity': entitylist,
        'Count': counts
    })
    plt.figure(figsize=(14, 8))
    sns.barplot(data=df, x='Region', y='Count', hue='Entity', dodge=True)  # dodge=True creates grouped bars

    plt.title('Self Regulation Initiative Counts Across Different Regions')
    plt.xlabel('Region')
    plt.ylabel('Count')
    plt.xticks(rotation=45)

    # Adjust legend
    plt.legend(title='Entity', loc='upper right', fontsize='small', bbox_to_anchor=(1.15, 1))

    # Optionally, adjust margins
    plt.subplots_adjust(right=0.85)
    plt.show()


def tracking_tech():
    regions = []
    entitylist = []
    counts = []
    trackings = ['Cookies', 'Web Beacon', 'Supercookies']
    trackingnames = ['Cookies', 'Beacon', 'Supercookies']
    pattern_dict = {}
    for i in range(3):
        pattern_dict[trackings[i]] = re.compile(re.escape(trackingnames[i]), re.IGNORECASE)

    i = 0
    with open('./nltk_results/nltk_results3.json', 'r', encoding='utf-8') as json_file:
        entities = json.load(json_file)
        print("successfully load file")
        # compile the re patttern for the six third parties
        for region in entities.keys():
            print(f"start on region {region}")
            entity_counts = {'Cookies': 0, 'Web Beacon': 0, 'Supercookies': 0}
            for name in entities[region]:
                # print(name)
                for entity_word, pattern in pattern_dict.items():
                    if pattern.search(name):
                        entity_counts[entity_word] += 1

            for i in entity_counts.keys():
                regions.append(region)
                entitylist.append(i)
                counts.append(entity_counts[i])

    df = pd.DataFrame({
        'Region': regions,
        'Entity': entitylist,
        'Count': counts
    })
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df, x='Region', y='Count', hue='Entity', dodge=True)  # dodge=True creates grouped bars

    plt.title('Tracking technology Counts Across Different Regions')
    plt.xlabel('Region')
    plt.ylabel('Count')
    plt.xticks(rotation=45)

    # Adjust legend
    plt.legend(title='Entity', loc='upper right', fontsize='small', bbox_to_anchor=(1.15, 1))

    # Optionally, adjust margins
    plt.subplots_adjust(right=0.85)
    plt.show()


def third_party():
    regions = []
    entitylist = []
    counts = []
    third_parties = ['Google', 'Facebook', 'Twitter', 'Amazon', 'Yahoo', 'AOL']
    pattern_dict = {entity_word: re.compile(re.escape(entity_word), re.IGNORECASE) for entity_word in third_parties}

    # for entity_word in third_parties:
    #     pattern = re.compile(re.escape(entity_word), re.IGNORECASE)
    i = 0
    with open('./nltk_results/nltk_results3.json', 'r', encoding='utf-8') as json_file:
        entities = json.load(json_file)
        print("successfully load file")
        # compile the re patttern for the six third parties
        for region in entities.keys():
            print(f"start on region {region}")
            entity_counts = {'Google': 0, 'Facebook': 0, 'Twitter': 0, 'Amazon': 0, 'Yahoo': 0, 'AOL': 0}
            for name in entities[region]:
                # print(name)
                for entity_word, pattern in pattern_dict.items():
                    if pattern.search(name):
                        entity_counts[entity_word] += 1


            for i in entity_counts.keys():
                regions.append(region)
                entitylist.append(i)
                counts.append(entity_counts[i])

    df = pd.DataFrame({
        'Region': regions,
        'Entity': entitylist,
        'Count': counts
    })
    plt.figure(figsize=(14, 8))
    sns.barplot(data=df, x='Region', y='Count', hue='Entity', dodge=True)  # dodge=True creates grouped bars


    plt.title('Third-Party Entity Counts Across Different Regions')
    plt.xlabel('Region')
    plt.ylabel('Count')
    plt.xticks(rotation=45)

    # Adjust legend
    plt.legend(title='Entity', loc='upper right', fontsize='small', bbox_to_anchor=(1.15, 1))

    # Optionally, adjust margins
    plt.subplots_adjust(right=0.85)
    plt.show()




def fetch_entity1():
    obj = {}
    for region in os.listdir('./final1'):
        print("region")
        l = find_entity(region)
        if region not in obj.keys():
            obj[region] = l

    json_file_path = os.path.join('./entity_res', "entities.json")

    # Save the entities to a JSON file
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(obj, json_file, ensure_ascii=False, indent=4)


        # print("Now processing ", region, '\n')




def find_entity(region, stop = False):
    l = []
    print("Start working on region: ", region, '\n')
    folder_path = './final1'
    i = 1
    for filename in os.listdir(f'{folder_path}/{region}'):
        nlp.max_length = 2000000
        if filename.endswith(".md"):  # Check if the file is a markdown file
            print(i)
            i += 1
            file_path = os.path.join(f'{folder_path}/{region}', filename)
            text = collect(file_path)
            doc = nlp(text)
        else:
            break

        for ent in doc.ents:
            l.append(ent.text)
            # print(ent.label_, ent.text)

    return l



    # return l




def movetwo():
    res = {}

    with open('./entity_res/entities.json', 'r', encoding='utf-8') as json_file:
        entities = json.load(json_file)
        res = entities

    with open('./entity_res/entities1.json', 'r', encoding='utf-8') as f:
        newtwo = json.load(f)
        entities['br'] = newtwo['br']
        entities['de'] = newtwo['de']

    json_file_path = os.path.join('./entity_res', "entities3.json")

    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(entities, json_file, ensure_ascii=False, indent=4)


def entity_frequency():
    entities = {}
    # top_entities = {}
    #
    with open('./entity_res/entities3.json', 'r', encoding='utf-8') as f:
        entities = json.load(f)

    # print("load successfully")
    # for key in entities.keys():
    #
    #     entities_freq = Counter(entities[key])
    #     sorted_bigrams = sorted(entities_freq.items(), key=lambda x: x[1], reverse=True)
    #     top_entities[key] = sorted_bigrams[:10]
    #
    # output_path = os.path.join('./entity_res', f"entities_frequency.json")
    #
    # # dump the all country frequency results into json
    # with open(output_path, 'w', encoding='utf-8') as f:
    #     json.dump(top_entities, f, ensure_ascii=False,indent=4)

    print("start processing the top 10 frequency of all regions")
    biglist = []
    for key in entities.keys():
        biglist = biglist + entities[key]

    patterns = [re.compile(re.escape('zoom'), re.IGNORECASE), re.compile(re.escape('third'), re.IGNORECASE),
                re.compile(re.escape('one'), re.IGNORECASE)]

    reslist = []
    for word in biglist:
        flag = False
        for pattern in patterns:
            if pattern.findall(word):
                flag = True
                break
        if not flag:
            reslist.append(word)

    obj = {}
    sorted_all = Counter(reslist)
    all_freq = sorted(sorted_all.items(), key=lambda x: x[1], reverse=True)[:10]
    print(all_freq)
    obj['all'] = all_freq
    with open('./entity_res/all_frequency_withoutzoom.json', 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False,indent=4)

# draw the entity of all regions combined
def draw_all_freq():
    data = {}
    with open('./entity_res/all_frequency_withoutzoom.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    entities = [item[0] for item in data["all"]]
    counts = [item[1] for item in data["all"]]

    # Creating the bar graph
    plt.figure(figsize=(20, 20))  # Set the figure size
    plt.bar(entities, counts, color='skyblue')  # Create a bar chart

    plt.xlabel('Entity')  # Label for X-axis
    plt.ylabel('Frequency')  # Label for Y-axis
    plt.title('Top 10 Entities Frequency(After filtering)')  # Title of the graph
    plt.xticks(rotation=45, ha='right')  # Rotate the X-axis labels for better readability

    plt.tight_layout()  # Automatically adjust subplot parameters to give specified padding
    plt.show()  # Display the graph


# draw the entity list of each country
def draw_each():
    data = {}
    with open('./entity_res/entities.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    patterns = []
    l = ['1','2','3','4','5','6','7','8','one','third','two']
    for i in l:
        patterns.append(re.compile(re.escape(i), re.IGNORECASE))
    # patterns = [re.compile(re.escape('1'), re.IGNORECASE), re.compile(re.escape('2'), re.IGNORECASE),
    #             re.compile(re.escape('third'), re.IGNORECASE)]
    # print("successully loaded")
    try:
        for region in data.keys():
            reslist = []
            for word in data[region]:
                flag = False
                for pattern in patterns:
                    if pattern.findall(word):
                        flag = True
                        break
                if not flag:
                    reslist.append(word)

            sorted_all = Counter(reslist)
            all_freq = sorted(sorted_all.items(), key=lambda x: x[1], reverse=True)[:20]
            filter = []
            # for word in all_freq:
            #     if word in
            print(all_freq)
            entities = [item[0] for item in all_freq]
            counts = [item[1] for item in all_freq]

            # Creating the bar graph
            plt.figure(figsize=(20, 20))  # Set the figure size
            plt.bar(entities, counts, color='skyblue')  # Create a bar chart

            plt.xlabel('Entity')  # Label for X-axis
            plt.ylabel('Frequency')  # Label for Y-axis
            plt.title('Top 10 Entities Frequency(After filtering)')  # Title of the graph
            plt.xticks(rotation=45, ha='right')  # Rotate the X-axis labels for better readability

            plt.tight_layout()  # Automatically adjust subplot parameters to give specified padding
            plot_save_path = os.path.join(f'./graphs/entity/', f'{region}.png')
            plt.savefig(plot_save_path)
            plt.close()
                 # Display the graphs
    except Exception as e:
        print(e)

if __name__=="__main__":
    # find_entity('us')
    # fetch_entity1()
    draw_each()
