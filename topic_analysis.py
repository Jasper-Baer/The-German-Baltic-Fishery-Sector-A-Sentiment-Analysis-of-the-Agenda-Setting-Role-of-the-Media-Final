# -*- coding: utf-8 -*-
"""
Created on Wed Jan  1 16:33:17 2025

@author: Jasper Bär
"""

import matplotlib.pyplot as plt
from matplotlib.transforms import offset_copy
from data_prep import sentiment_index_yearly, fishery_year

import pandas as pd
import os
import pickle

###############################################################################

start_year = 2009
end_year = 2022

quota_path = r'Data\data, fish & fisheries, SD22-24.xlsx'
quota_dates = pd.read_excel(quota_path, sheet_name='dates, advice - quota ')['quota decision']
quota_dates = quota_dates[(quota_dates.dt.year >= start_year) & (quota_dates.dt.year <= end_year)][:-1].reset_index(drop=True)

# path to party related sentences
party_data_path = r"D:\Studium\PhD\Github\Fischerei - Master\Manuall_Anot.xlsx"
#party_data_path = r"Data\party_sentences.xlsx"

###############################################################################

def load_object(name, dir='saved_objects'):
    path = os.path.join(dir, f"{name}.pkl")
    with open(path, 'rb') as f:
        return pickle.load(f)
    
analysis_results = load_object('analysis_results')

###############################################################################
# Generate figure 5
###############################################################################

def convert_color(rgb):
    return tuple(x / 255. for x in rgb)

color_politics = convert_color((0, 89, 84))
color_fishery  = convert_color((254, 217, 145))
color_science  = convert_color((99, 194, 203))
color_engo     = convert_color((244, 177, 131))

color_map_topic = {
    'politics|management': color_politics,
    'fisheries': color_fishery,
    'science': color_science,
    'engo': color_engo
}

color_map_party = {'CDU': 'black', 'GREENS': 'green', 'SPD': 'red', 'PPA_rest':'grey'}

numerical_mapping = {
   "Regulation": 0,
   "Science":1,
    "Nachhaltigkeit und Umweltschutz": 2,
    "Fischereihilfe und Unterstützung": 3,
    "Sonstiges": 4  
}

number_to_label = {v: k for k, v in numerical_mapping.items()}
grouped_mapping = {
    "Regulation": "Regulatory fishery law",
    "Science": "Scientific (Governance) advice",
    "Fischereihilfe und Unterstützung": "Fisheries subsides and \n institutional support",
    "Nachhaltigkeit und Umweltschutz": "Environmental and \n nature conservation",
    "Sonstiges": "Other"
}
labels_topic = [
    "Regulatory fishery law",
    "Scientific (Governance) advice",
    'Fisheries subsides and \n institutional support',
    'Environmental and \n nature conservation',
    'Other'
]

label_map_party = {
    'CDU': 'CDU',
    'GREENS': 'Greens',
    'SPD': 'SPD',
    'PPA_rest': 'PPA Other'
}
label_map_topic = {
    'politics|management': 'Politics & Public Authorities',
    'fisheries': 'Fishery',
    'science': 'Science',
    'engo': 'eNGO'
}

# Load sentences labeled with topics
data_main = pd.read_csv(r'Data\fishery_lemmas_sentences_labeled_topic_30_07.csv', low_memory=False)

fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(20,6))

categories_topic = ['fisheries', 'engo', 'politics|management', 'science']
means_topic = {category: [] for category in categories_topic}

for category in categories_topic:
    subset = analysis_results[category][6]['text']
    subset_data = data_main[data_main['text'].isin(subset)].copy()
    subset_data['Year'] = pd.to_datetime(subset_data['Date'], errors='coerce').dt.year
    subset_data['Label_name'] = subset_data['Label'].map(number_to_label)
    subset_data['Grouped_Label'] = subset_data['Label_name'].map(grouped_mapping)
    yearly_share = subset_data.groupby(['Year', 'Grouped_Label']).size().unstack(fill_value=0).div(
        subset_data.groupby('Year').size(), axis=0) * 100
    yearly_share = yearly_share[2:]
    mean_shares = yearly_share.mean()
    for label in labels_topic:
        means_topic[category].append(mean_shares.get(label, 0))

mean_df_topic = pd.DataFrame(means_topic, index=labels_topic)
mean_df_topic.plot(kind='bar', 
                   ax=ax1, 
                   color=[color_map_topic[cat] for cat in categories_topic],
                   width=0.8)
ax1.set_ylabel('Topic Share (%)', fontsize=24)
ax1.legend_.remove()
plt.sca(ax1)
plt.xticks(rotation=45, ha='right')
handles1, labels1 = ax1.get_legend_handles_labels()
labels1 = [label_map_topic.get(label, label) for label in labels1]
ax1.tick_params(axis='y', labelsize=18)
ax1.tick_params(axis='x', labelsize=12)
xticklabels = ax1.get_xticklabels()

for i, label in enumerate(xticklabels):
    offset = 20
    if i in [1]:
        offset = 30  
    if i in [2]:
        offset = 40  
    label.set_transform(offset_copy(label.get_transform(), x=offset, y=0, units='dots'))

for bar in ax1.patches:
    height = bar.get_height()
    ax1.annotate(f'{height:.1f}%',
                 xy=(bar.get_x() + bar.get_width()/2, height),
                 xytext=(0,3),
                 textcoords="offset points",
                 ha='center',
                 va='bottom',
                 fontsize=9)

categories_party = ['CDU', 'GREENS', 'SPD', 'PPA_rest']
means_party = {category: [] for category in categories_party}

for category in categories_party:
    subset = pd.read_excel(party_data_path, sheet_name=category)['text']
    subset_data = data_main[data_main['text'].isin(subset)].copy()
    subset_data["Date"] = pd.to_datetime(subset_data["Date"], format='%Y-%m-%d')
    subset_data['Year'] = pd.to_datetime(subset_data['Date'], errors='coerce').dt.year
    subset_data['Label_name'] = subset_data['Label'].map(number_to_label)
    subset_data['Grouped_Label'] = subset_data['Label_name'].map(grouped_mapping)
    yearly_share = subset_data.groupby(['Year', 'Grouped_Label']).size().unstack(fill_value=0).div(
        subset_data.groupby('Year').size(), axis=0) * 100
    mean_shares = yearly_share.mean()
    for label in labels_topic:
        means_party[category].append(mean_shares.get(label, 0))

mean_df_party = pd.DataFrame(means_party, index=labels_topic)
mean_df_party.plot(kind='bar', ax=ax2, color=[color_map_party[cat] for cat in categories_party])
ax2.legend_.remove()
plt.sca(ax2)
plt.xticks(rotation=45, ha='right')
handles2, labels2 = ax2.get_legend_handles_labels()
labels2 = [label_map_party.get(label, label) for label in labels2]
ax2.tick_params(axis='y', labelsize=18)
ax2.tick_params(axis='x', labelsize=12)
xticklabels = ax2.get_xticklabels()

for i, label in enumerate(xticklabels):
    offset = 20
    if i in [1]:
        offset = 30  
    if i in [2]:
        offset = 40  
    label.set_transform(offset_copy(label.get_transform(), x=offset, y=0, units='dots'))

for bar in ax2.patches:
    height = bar.get_height()
    ax2.annotate(f'{height:.1f}%',
                 xy=(bar.get_x() + bar.get_width()/2, height),
                 xytext=(0,3),
                 textcoords="offset points",
                 ha='center',
                 va='bottom',
                 fontsize=9)

fig.legend(handles1, labels1,
           loc='lower left',
           bbox_to_anchor=(0.05, -0.25),
           ncol=4,
           fontsize=16,
           frameon=False)

fig.legend(handles2, labels2,
           loc='lower right',
           bbox_to_anchor=(0.95, -0.25),
           ncol=4,
           fontsize=16,
           frameon=False)

ax1.set_title('(a) Stakeholder Groups', y=-0.55, fontsize=16)
ax2.set_title('(b) Parties', y=-0.55, fontsize=16)

fig.subplots_adjust(left=0.07, right=0.975, top=0.95, bottom=0.15)

plt.savefig(r'Figures\figure5.svg', format='svg', dpi=500, bbox_inches='tight')
plt.savefig(r'Figures\figure5.eps', format='eps', dpi=500, bbox_inches='tight')
plt.show()

###############################################################################
# Generate data for tables S11, S12 and 2(c)
###############################################################################

data = pd.read_csv(r'Data\fishery_lemmas_sentences_labeled_fishery_stance.csv', low_memory=False)
#data = pd.read_csv(r'Data\fishery_lemmas_sentences_labeled_sentiment.csv', low_memory=False)

categories = ['CDU', 'GREENS', 'SPD', 'PPA_rest']
color_map = {'CDU': 'black', 'GREENS': 'green', 'SPD': 'red', 'PPA_rest':'grey'}
label_map = {'CDU': 'CDU', 'GREENS': 'Greens', 'SPD': 'SPD', 'PPA_rest':'PPA Other'}

stats_list = []

for category in categories:

    subset = pd.read_excel(party_data_path, sheet_name=category)['text']
    subset_data = data[data['text'].isin(subset)].copy()

    subset_data["Date"] = pd.to_datetime(subset_data["Date"], format='%Y-%m-%d')
    subset_data['Year'] = pd.to_datetime(subset_data['Date'], errors='coerce').dt.year

    yearly_share = sentiment_index_yearly(fishery_year(subset_data, quota_dates))[['year','Sentiment Index']]
    yearly_share.index = quota_dates[:-1]

    if category == 'GREENS':
        yearly_share = yearly_share[2:]
    
    desc = yearly_share['Sentiment Index'].describe()
    stats_list.append({
        'Party': label_map[category],
        'Mean': desc['mean'],
        'Std': desc['std'],
        'Min': desc['min'],
        'Max': desc['max']
    })

stats_df = pd.DataFrame(stats_list)
stats_df.to_excel(f'Results_new\party_stats.xlsx', index=False)
