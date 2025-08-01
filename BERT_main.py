# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 22:16:36 2021

@author: Jasper Bär
"""

import torch
import pandas as pd
from transformers import BertForSequenceClassification, AdamW, get_linear_schedule_with_warmup, BertTokenizer
from BERT_preprocess import prepare_training_data, prepare_inference_data
from BERT_train_test_predict import train, test, predict

###############################################################################
### Train and test BERT model for sentiment classification
###############################################################################

# Load training data
# data = pd.read_excel(r'data_train_sentiment.xlsx')
# data = pd.read_excel(r'data_train_fishery_stance.xlsx')
# data = pd.read_excel(r'data_train_topic.xlsx')

# Set path for storing the trained model
#PATH = r"Data\fishery_model_sentiment.pt"
#PATH = r"Data\fishery_model_fishery_stance.pt"
#PATH = r"Data\fishery_model_topic.pt"

seed = 0

# Torch RNG
torch.manual_seed(seed)
torch.cuda.manual_seed_all(seed)

# Select max sentence length
max_len = 100

# Select a batch size for training.
batch_size = 32

# Set word embedding model
word_embedding = "deepset/gbert-base"

learning_rate = 2e-5

epochs = 6

train_on_gpu = True

#lr_scheduler = get_linear_schedule_with_warmup(optimizer, num_training_steps = max_train_steps, num_warmup_steps=0)
lr_scheduler = None

# Transform data and split them into train, validation and test data
train_dataloader, test_dataloader, validation_dataloader = prepare_training_data(data, max_len, batch_size, word_embedding)

# Select classification layer 
bert_type = 'Sequence'

if bert_type == 'Sequence':
    model =  BertForSequenceClassification.from_pretrained(word_embedding, num_labels=5)
else:
    print('Please set bert_type as LSTM or Sequence')    

# Get all parameters from BERT embedding layers
pretrained_names = [f'bert.{k}' for (k, v) in model.bert.named_parameters()]

# Get all parameters from the classification layer
new_params= [v for k, v in model.named_parameters() if k not in pretrained_names]

param_optimizer = list(model.named_parameters())
no_decay = ['bias', 'gamma', 'beta']
optimizer_grouped_parameters = [
    {'params': [p for n, p in param_optimizer if not any(nd in n for nd in no_decay)],
     'weight_decay_rate': 0.01},
    {'params': [p for n, p in param_optimizer if any(nd in n for nd in no_decay)],
     'weight_decay_rate': 0.0}
]

max_train_steps = len(train_dataloader) * epochs

optimizer = AdamW(optimizer_grouped_parameters, lr=learning_rate, correct_bias=False)

train(PATH, epochs, model, bert_type, optimizer, lr_scheduler, train_on_gpu, train_dataloader, validation_dataloader)

model.load_state_dict(torch.load(PATH))       

# Change 3 to 5 for topic classification model
f1_score = test(model, bert_type, train_on_gpu, test_dataloader, 3)

###############################################################################
### Classifiy sentiment, fishery stance and topic of all sentences in our dataset
###############################################################################

tokenizer = BertTokenizer.from_pretrained(word_embedding, do_lower_case=True)

data_sents = pd.read_csv(r'Data\fishery_lemmas_sentences.csv')

dataloader = prepare_inference_data(data_sents, tokenizer, 100)
data_sents["Label"] = predict(model, bert_type, train_on_gpu, dataloader)

#data_sents.to_csv(r'Data\fishery_lemmas_sentences_labeled_sentiment.csv')
#data_sents.to_csv(r'Data\fishery_lemmas_sentences_labeled_fishery_stance.csv')
#data_sents.to_csv(r'Data\fishery_lemmas_sentences_labeled_topic.csv')
