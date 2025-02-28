# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 20:20:28 2025

@author: Ja-ba
"""

import pickle
import re
import pandas as pd
import spacy

from nltk.corpus import stopwords

def load_object(name, dir='saved_objects'):
    path = os.path.join(dir, f"{name}.pkl")
    with open(path, 'rb') as f:
        return pickle.load(f)
    
analysis_results = load_object('analysis_results')

def make_safe_filename(title):
    filename = title.lower().replace(' ', '_')
    filename = re.sub(r'[^a-z0-9_]+', '', filename)
    filename += '.png'
    return filename

def map_name_to_subfolder(name):
    mapping = {
        'Greens_all': "Greens",
        'Greens_neg': "Greens",
        'Greens_neu': "Greens",
        'Greens_pos': "Greens",
        'engo_all': "Environment",
        'engo_neg': "Environment",
        'engo_neut': "Environment",
        'engo_pos': "Environment",
        'fish_all': "Fishers",
        'fish_neg': "Fishers",
        'fish_neut': "Fishers",
        'fish_pos': "Fishers",
        'sci_all': "Science",
        'sci_neg': "Science",
        'sci_neut': "Science",
        'sci_pos': "Science",
        'pm_all': "Politics & Management",
        'pm_neg': "Politics & Management",
        'pm_neut': "Politics & Management",
        'pm_pos': "Politics & Management"
    }
    return mapping.get(name, "Unknown")

# Datasets Dictionary
datasets = {
    
    "engo_all": pd.concat([df['text'] for df in analysis_results['engo'][6:8]]),
    "engo_neg": pd.concat([df.loc[df['Label'] == 0, 'text'] for df in analysis_results['engo'][6:8]]),
    "engo_neut": pd.concat([df.loc[df['Label'] == 1, 'text'] for df in analysis_results['engo'][6:8]]),
    "engo_pos": pd.concat([df.loc[df['Label'] == 2, 'text'] for df in analysis_results['engo'][6:8]]),

    "fish_all": pd.concat([df['text'] for df in analysis_results['fisheries'][6:8]]),
    "fish_neg": pd.concat([df.loc[df['Label'] == 0, 'text'] for df in analysis_results['fisheries'][6:8]]),
    "fish_neut": pd.concat([df.loc[df['Label'] == 1, 'text'] for df in analysis_results['fisheries'][6:8]]),
    "fish_pos": pd.concat([df.loc[df['Label'] == 2, 'text'] for df in analysis_results['fisheries'][6:8]]),

    "sci_all": pd.concat([df['text'] for df in analysis_results['science'][6:8]]),
    "sci_neg": pd.concat([df.loc[df['Label'] == 0, 'text'] for df in analysis_results['science'][6:8]]),
    "sci_neut": pd.concat([df.loc[df['Label'] == 1, 'text'] for df in analysis_results['science'][6:8]]),
    "sci_pos": pd.concat([df.loc[df['Label'] == 2, 'text'] for df in analysis_results['science'][6:8]]),
    
    "pm_all": pd.concat([df['text'] for df in analysis_results['politics|management'][6:8]]),
    "pm_neg": pd.concat([df.loc[df['Label'] == 0, 'text'] for df in analysis_results['politics|management'][6:8]]),
    "pm_neut": pd.concat([df.loc[df['Label'] == 1, 'text'] for df in analysis_results['politics|management'][6:8]]),
    "pm_pos": pd.concat([df.loc[df['Label'] == 2, 'text'] for df in analysis_results['politics|management'][6:8]])
}

# Load SpaCy model
nlp = spacy.load("de_core_news_lg", disable=["parser", "ner"])

# Define desired POS options
desired_pos_options = [
    #    ["NOUN"]
 #   ["ADV", "ADJ", "VERB"],
    ["ADV", "ADJ", "VERB", "NOUN"],
]

base_stopwords = set(stopwords.words('german'))

all_names = []

for full_name in common_pers['Name']:
    parts = full_name.strip().split()
    first_name = parts[0]
    last_name = parts[-1] if len(parts) > 1 else ''
    all_names.extend([first_name, last_name])

base_stopwords.update(all_names)

# Filter out all names of stakeholders and words which have no meaning on their own
base_stopwords.update(['grüne', 'agrarminister', 'fischereiminister', 'umweltminister', 'bundeslandwirtschaftsministerin',
'landwirtschaftsminister', 'land', 'bundeslandwirtschaftsminister', 'bundesagrarministerin', 'minister'])

base_stopwords.update(['schon', 'mal', 'sagen', 'mehr', 'kommen', 'gehen', 'fast', 'jahr', 'prozent'])

base_stopwords.update(['kieler', 'rostocker', 'westlich', 'deutsch'])

base_stopwords.update(['fischer', 'fisch', 'küstenfischer','ostseefischerei', 'küstenfischerei',
                       'fischerei', 'umweltorganisation', 'umweltschutzorganisation', 'fischereigenossenschaft',
                       'landesfischereiverband', 'vorsitzend', 'landesverband', 'verband'])

base_stopwords.update(['umweltorganisation', 'umweltschutzorganisation'])

base_stopwords.update(['rat', 'international', 'leiter', 'direktor', 'institut', 'wissenschaftler'])

base_stopwords = list(base_stopwords)
base_stopwords = [word.lower() for word in base_stopwords]

###############################################################################

import os
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
from tqdm import tqdm

for desired_pos in desired_pos_options:
    desired_pos_folder = "_".join(desired_pos)
    save_excel_dir = os.path.join("wordcloud", desired_pos_folder)
    os.makedirs(save_excel_dir, exist_ok=True)
    excel_filename = os.path.join(save_excel_dir, f"{desired_pos_folder}_tables.xlsx")
    
    with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
        for name, text_series in tqdm(datasets.items(), desc=f"Processing for {desired_pos_folder}"):
            
            text_series = datasets[name]
            text_data = " ".join(text_series)
            nlp.max_length = len(text_data) + 100
            doc = nlp(text_data)
            filtered_tokens = []
            for token in doc:
                if (token.pos_ in desired_pos and 
                    token.is_alpha and 
                    token.lemma_.lower() not in base_stopwords):
                    filtered_tokens.append(token.lemma_.lower())
                    
            unigram_counts = Counter(filtered_tokens)
            filtered_unigrams = {
                word: count 
                for word, count in unigram_counts.items() 
                if count >= 3 and word not in base_stopwords
            }
            
            sorted_words = sorted(filtered_unigrams.items(), key=lambda x: x[1], reverse=True)
            top15_words = sorted_words[:20]
            top15_dict = dict(top15_words)
            
            filtered_text = " ".join(filtered_tokens)
            
            df_freq = pd.DataFrame(filtered_unigrams.items(), columns=['Word', 'Frequency'])
            df_freq = df_freq.sort_values(by='Frequency', ascending=False).head(20)
            print("Most frequent words for", name, str(desired_pos))
            print(df_freq)
            
            subfolder = map_name_to_subfolder(name)
            full_save_dir = os.path.join("wordcloud", desired_pos_folder, subfolder)
            os.makedirs(full_save_dir, exist_ok=True)
            
            filename = make_safe_filename(f"Results_new\{desired_pos_folder}_{name}_wordcloud")
            full_file_path = os.path.join(full_save_dir, filename)
            
            print(f"Saved plot: {full_file_path}")
            
            df_freq.to_excel(writer, sheet_name=name, index=False)