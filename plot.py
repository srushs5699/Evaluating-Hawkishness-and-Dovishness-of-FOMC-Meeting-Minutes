import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline
import re

# Load the polarity score files
speeches_polarity_df = pd.read_csv('./all_fed_speeches_with_polarity.csv')
minutes_polarity_df = pd.read_csv('./df_minutes_with_polarity.csv')
press_conferences_polarity_df = pd.read_csv('./df_press_conferences_with_polarity.csv')

# Load the bond market data from Excel file
xls = pd.ExcelFile('./FOMC_Data_2011_2024.xlsx')
gt10_df = pd.read_excel(xls, 'GT10')
gt2_df = pd.read_excel(xls, 'GT2')
spread_df = pd.read_excel(xls, '2s10s_Spread')

# Convert the 'date' columns to datetime
speeches_polarity_df['date'] = pd.to_datetime(speeches_polarity_df['date'])
minutes_polarity_df.rename(columns={'Unnamed: 0': 'date'}, inplace=True)
minutes_polarity_df['date'] = pd.to_datetime(minutes_polarity_df['date'])
press_conferences_polarity_df.rename(columns={'Unnamed: 0': 'date'}, inplace=True)
press_conferences_polarity_df['date'] = pd.to_datetime(press_conferences_polarity_df['date'])
gt10_df['Date'] = pd.to_datetime(gt10_df['Date'])
gt2_df['Date'] = pd.to_datetime(gt2_df['Date'])
spread_df['Date'] = pd.to_datetime(spread_df['Date'])

# Function to merge polarity scores with bond market data
def merge_polarity_with_bond_data(polarity_df, title):
    merged_df = pd.merge(polarity_df, gt10_df[['Date', 'PX_MID']], left_on='date', right_on='Date', how='left')
    merged_df = pd.merge(merged_df, gt2_df[['Date', 'PX_MID']], left_on='date', right_on='Date', how='left', suffixes=('_10y', '_2y'))
    merged_df = pd.merge(merged_df, spread_df[['Date', 'PX_LAST']], left_on='date', right_on='Date', how='left')
    merged_df = merged_df.drop(columns=['Date_10y', 'Date_2y', 'Date'])
    
    # Rename the columns for clarity
    merged_df.rename(columns={'PX_MID_10y': '10y_yield', 'PX_MID_2y': '2y_yield', 'PX_LAST': '2s10s_spread'}, inplace=True)
    
    return merged_df

# Merge the polarity data with bond market data
merged_speeches_df = merge_polarity_with_bond_data(speeches_polarity_df, "Speeches")
merged_minutes_df = merge_polarity_with_bond_data(minutes_polarity_df, "Minutes")
merged_press_conferences_df = merge_polarity_with_bond_data(press_conferences_polarity_df, "Press Conferences")

# Function to compute and save correlation matrix
def correlation_analysis(df, title, filename):
    relevant_columns = ['score', '10y_yield', '2y_yield', '2s10s_spread']
    correlation_matrix = df[relevant_columns].corr()

    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', vmin=-1, vmax=1)
    plt.title(f'Correlation Matrix: {title}')
    
    # Save the correlation heatmap
    plt.savefig(f"{filename}_correlation_matrix.png")
    plt.close()

# Function to visualize trends and save as image
def visualize_trends(df, title, filename):
    plt.figure(figsize=(12, 8))

    plt.subplot(3, 1, 1)
    plt.plot(df['date'], df['score'], label='Polarity Score', color='purple')
    plt.title(f'Polarity Score over Time: {title}')
    plt.ylabel('Polarity Score')
    plt.grid(True)

    plt.subplot(3, 1, 2)
    plt.plot(df['date'], df['10y_yield'], label='10-Year Yield', color='blue')
    plt.title('10-Year Yield over Time')
    plt.ylabel('10-Year Yield')
    plt.grid(True)

    plt.subplot(3, 1, 3)
    plt.plot(df['date'], df['2s10s_spread'], label='2s10s Spread', color='green')
    plt.title('2s10s Spread over Time')
    plt.ylabel('2s10s Spread')
    plt.grid(True)

    # Save the plot as an image
    plt.tight_layout()
    plt.savefig(f"{filename}_trends.png")
    plt.close()

# Correlation analysis and visualization for each dataset
correlation_analysis(merged_speeches_df.dropna(), "Speeches Polarity and Bond Market Yields", "speeches")
correlation_analysis(merged_minutes_df.dropna(), "Minutes Polarity and Bond Market Yields", "minutes")
correlation_analysis(merged_press_conferences_df.dropna(), "Press Conferences Polarity and Bond Market Yields", "press_conferences")

visualize_trends(merged_speeches_df.dropna(), "Speeches", "speeches")
visualize_trends(merged_minutes_df.dropna(), "Minutes", "minutes")
visualize_trends(merged_press_conferences_df.dropna(), "Press Conferences", "press_conferences")
