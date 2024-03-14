# Privacy-Policy-Analysis

This is a project I did with Justin Dong (https://github.com/justin-e-dong) and Jerry Cao (https://github.com/Jiarui-Cao). 
This directory contains only my portion, which does not include the crawler we built. 


To run the analysis scripts, you need to first install all packages specified in requirements.txt.

Here are the brief summary of each files:

Length.py: The length analysis
newngram.py: The newest ngram script, newngram() is responsible for generate ngram charts for each nation, nltk_store() is responsible for storing the results from md files into json files for further analysis.
markdown_to_text.py: a preprocessing script
entity.py: The script that is responsible for generating an json file that stores the entity information of each region with all functions responsible for analyzing the entity names and term surfacing
filtering.py: filter the biggest overlapping dataset.

You might need to manually create change the folder paths based on what is specified in the functions. The raw md files we crawled are at this link:







