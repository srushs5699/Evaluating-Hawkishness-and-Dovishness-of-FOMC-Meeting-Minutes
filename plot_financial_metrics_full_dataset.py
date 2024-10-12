import pandas as pd
import matplotlib.pyplot as plt

# Plotting function for yearly trends
def plot_yearly_trends(yearly_similarity, yearly_metric, metric_name):
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plot hawkish similarity score per year
    ax1.plot(yearly_similarity['year'], yearly_similarity['hawkish_similarity'], color='purple', label='Hawkish Similarity Score')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Hawkish Similarity Score')

    # Plot the financial metric on a secondary axis
    ax2 = ax1.twinx()
    ax2.plot(yearly_metric['year'], yearly_metric.iloc[:, 1], color='green', label=metric_name, alpha=0.6)
    ax2.set_ylabel(metric_name)

    fig.legend(loc='upper right', bbox_to_anchor=(0.9, 0.85))
    plt.title(f'Yearly Trend of Hawkish Similarity Score and {metric_name}')
    plt.show()

# Assuming 'classification_results_df', 'sp500_data', 'vix_data', 'gold_prices', 'spread_2s10s', 'yield_2yr', 'yield_10yr' are loaded
classification_results_df = pd.read_csv('FOMC_classification_results.csv')

fomc_data = pd.ExcelFile('./FOMC_Data_2011_2024.xlsx')

# Load the relevant sheets into dataframes
sp500_data = pd.read_excel(fomc_data, sheet_name='SP500')
vix_data = pd.read_excel(fomc_data, sheet_name='VIX')
gold_prices = pd.read_excel(fomc_data, sheet_name='Gold_Prices')
spread_2s10s = pd.read_excel(fomc_data, sheet_name='2s10s_Spread')
yield_2yr = pd.read_excel(fomc_data, sheet_name='GT2')
yield_10yr = pd.read_excel(fomc_data, sheet_name='GT10')

# Ensure the Date columns are converted to datetime format
sp500_data['Date'] = pd.to_datetime(sp500_data['Date'])
vix_data['Date'] = pd.to_datetime(vix_data['Date'])
gold_prices['Date'] = pd.to_datetime(gold_prices['Date'])
spread_2s10s['Date'] = pd.to_datetime(spread_2s10s['Date'])
yield_2yr['Date'] = pd.to_datetime(yield_2yr['Date'])
yield_10yr['Date'] = pd.to_datetime(yield_10yr['Date'])

# Extracting the year from the date column
classification_results_df['year'] = classification_results_df['date'].dt.year
sp500_data['year'] = sp500_data['Date'].dt.year
vix_data['year'] = vix_data['Date'].dt.year
gold_prices['yeacr'] = gold_prices['Date'].dt.year
spread_2s10s['year'] = spread_2s10s['Date'].dt.year
yield_2yr['year'] = yield_2yr['Date'].dt.year
yield_10yr['year'] = yield_10yr['Date'].dt.year

# Grouping by year to calculate yearly averages
yearly_similarity = classification_results_df.groupby('year')['hawkish_similarity'].mean().reset_index()
yearly_sp500 = sp500_data.groupby('year')['PX_LAST'].mean().reset_index()
yearly_vix = vix_data.groupby('year')['PX_LAST'].mean().reset_index()
yearly_gold = gold_prices.groupby('year')['PX_LAST'].mean().reset_index()
yearly_spread_2s10s = spread_2s10s.groupby('year')['PX_LAST'].mean().reset_index()
yearly_yield_2yr = yield_2yr.groupby('year')['PX_MID'].mean().reset_index()
yearly_yield_10yr = yield_10yr.groupby('year')['PX_MID'].mean().reset_index()

# Plotting yearly trends for each financial metric
plot_yearly_trends(yearly_similarity, yearly_sp500, 'S&P 500')
plot_yearly_trends(yearly_similarity, yearly_vix, 'VIX')
plot_yearly_trends(yearly_similarity, yearly_gold, 'Gold Prices')
plot_yearly_trends(yearly_similarity, yearly_spread_2s10s, '2s10s Spread')
plot_yearly_trends(yearly_similarity, yearly_yield_2yr, '2-Year Yield')
plot_yearly_trends(yearly_similarity, yearly_yield_10yr, '10-Year Yield')
