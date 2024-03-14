# This


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
import numpy as np
from ngrams import collect


def calculate_statistics(folder_path):
    stats = {}
    for region in os.listdir(folder_path):
        print(f"processing {region}")
        char_counts = []
        region_path = os.path.join(folder_path, region)
        for filename in os.listdir(region_path):
            file_path = os.path.join(region_path, filename)
            text = collect(file_path)
            char_counts.append(len(text))

        if char_counts:
            stats[region] = {
                'avg': np.mean(char_counts),
                'max': np.max(char_counts),
                'min': np.min(char_counts),
                '25th': np.percentile(char_counts, 25),
                '75th': np.percentile(char_counts, 75)
            }
    return stats


def plot_statistics(stats):
    regions = list(stats.keys())
    averages = [stats[region]['avg'] for region in regions]
    max_values = [stats[region]['max'] for region in regions]
    min_values = [stats[region]['min'] for region in regions]
    percentile_25th = [stats[region]['25th'] for region in regions]
    percentile_75th = [stats[region]['75th'] for region in regions]

    x = np.arange(len(regions))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, averages, width, label='Average')
    rects2 = ax.bar(x + width / 2, max_values, width, label='Max', alpha=0.5)
    rects3 = ax.bar(x + width / 2, min_values, width, label='Min', alpha=0.5)
    ax.plot(regions, percentile_25th, label='25th Percentile', color='green')
    ax.plot(regions, percentile_75th, label='75th Percentile', color='red')

    ax.set_xlabel('Region')
    ax.set_ylabel('Characters')
    ax.set_title('Character Counts by Region')
    ax.set_xticks(x)
    ax.set_xticklabels(regions)
    ax.legend()

    fig.tight_layout()

    plt.show()


if __name__ == "__main__":
    folder_path = './final3'
    stats = calculate_statistics(folder_path)
    plot_statistics(stats)
