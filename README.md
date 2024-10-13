# Evaluating-Hawkishness-and-Dovishness-of-FOMC-Meeting-Minute

In this project, we explore the sentiment of the Federal Open Market Committee (FOMC) communications over the past 13 years, focusing on Meeting Minutes, Fed speeches, and Press Conference transcripts. 

By utilizing FinBERT, a sentiment analysis model fine-tuned for financial texts, we assess the tone of these statements, categorizing them into "Hawkishness" and "Dovishness" based on the text in each document.

## Data collection:
This dataset includes FOMC Meeting Minutes, FOMC Press Conference and Fed speeches transcripts.

Step1:

fomc_meeting_minutes_data.py, fomc_press_conference_data.py, fomc_speeches_data.py are the respective files to download the mentioned data.
Initially, three different datasets were downloaded and analysis was carried on each one of them.

FOMC_Data_2011_2024.xlsx: This dataset contains the data for 10 year yield, 2 year yield, 2s10s spread, Gold prices, VIX, S&P 500 from 2012 to 2024.

Step 2:

After individual dataset analysis, we combined the three datasets into one and carried out the analysis on the same.


## Model

The model utilized to carry out the sentiment analysis was Finbert along with a Wordlist which occured frequently in the dataset.

polarity_scores_finbert.py: This file contains the steps to calculate the polarity score for each document on three different datasets.

FOMC classification.ipynb: This file contains the steps to calculate the polarity score and categorizing each document into hawkish or dovish sentiment based on their hawkish and dovish scores for the combined dataset.

## Analysis

In order to analyze how the hawkishness and dovishness of the fed meetings, press conferences and meeting minutes affected the market sentiments we plotted several graphs to deduce the trend.

The market indicators which were used  in this project were:

1. 10 year yield

2. 2 year yield

3. 2s10s spread

4. Gold prices

5. VIX

6. S&P 500

plot.py: this file contains the code to plot the individual datasets against the given market indicators.

plot_financial_metrics_full_dataset.py, FOMC Correlation.ipynb: this file contains the code to plot the full dataset against the given market indicators.







