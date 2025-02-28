# The-German-Baltic-Fishery-Sector-A-Sentiment-Analysis-of-the-Agenda-Setting-Role-of-the-Media

This repository includes the code for the generation of the results of our paper "The German Baltic Fishery Sector: A Sentiment Analysis of the Agenda-Setting Role of the Media".

**NOTE:** The original news articles used in the code cannot be openly published due to copyright restrictions. For any questions regarding the dataset, please contact the corresponding author.

**NOTE:** Addtional results and the trained sentiment model are available upon request.

## Files and Functions

- **load_data:** Loads the raw text files and stores them into a pandas DataFrame for further processing.

- **article_prep:** Contains functions to prepare the text data specific to fishery-related content.

- **data_prep:** Includes general functions to clean and prepare text data for subsequent steps.

- **article_distribution:** Analyzes the distribution of articles in the sample. Generates Figure 1 and Figure 2 (main text) and Figure S2 (appendix).

- **journal_filter:** Analyzes the composition of the sample in regard to the journals. Generates Table S3.

- **Bert_preprocess:** Contains all functions needed for preprocessing the textual data before using it with BERT.

- **Bert_train_test_predict:** Includes functions for training the BERT model and labeling the dataset after training.

- **Bert_main:** Preprocesses the textual data, trains the sentiment analysis model, and labels the sentences in the sample according to their sentiment.

- **sentiment_analysis:** Creates and analyzes the sentiment indices for the sample. Generates Table S5, Figure 3, Figure 4, and Figure S4.

- **named_entity_recognation:** Extracts all named entities from the sample, which are used for stakeholder analysis.

- **count_stakeholders:** Contains functions to count the number of organizational and individual stakeholders in given sentences.

- **stakeholder_analysis_util:** Contains several helper functions for the stakeholder analysis.

- **stakeholder_analysis:** Conducts the stakeholder analysis and generates Figure 5 and Tables S6, S7, S8, and S9.

## Data

- **data, fish & fisheries, SD22-24:** Includes the quotas and quota advices during the time of our sample.

- **entities_art:** Includes a list of all potential stakeholders based on the named entity recognition.

- **common_org_cleaned:** Includes all potential organizational stakeholders which we search for in our sample.

- **common_pers_cleaned:** Includes all potential individual stakeholders which we search for in our sample.

**NOTE:** Due to copyright restrictions, the raw data are not included in this repository. For any inquiries regarding the data, please contact the corresponding author.
