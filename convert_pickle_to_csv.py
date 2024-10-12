# code to convert df_minutes.pickle to df_minutes.csv

import pandas as pd
import pickle

# Load the pickle file
with open('df_minutes.pickle', 'rb') as f:
    df = pickle.load(f)

# Save the DataFrame to a CSV file
df.to_csv('df_minutes.csv', index=True)

print("Pickle file successfully converted to CSV!")

# code to convert df_press_conferences.pickle to df_press_conferences.csv

# # Load the pickle file
with open('df_press_conferences.pickle', 'rb') as f:
    df = pickle.load(f)

# Save the DataFrame to a CSV file
df.to_csv('df_press_conferences.csv', index=True)

print("Pickle file successfully converted to CSV!")

# code to convert all_fed_speeches.pickle to all_fed_speeches.csv

# Load the pickle file
with open('all_fed_speeches.pickle', 'rb') as f:
    df = pickle.load(f)

# Save the DataFrame to a CSV file
df.to_csv('all_fed_speeches.csv', index=True)

print("Pickle file successfully converted to CSV!")
