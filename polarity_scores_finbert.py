import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline
import re

# Load FinBERT model and tokenizer
finbert = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone', num_labels=3)
tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')

# Initialize the FinBERT pipeline
nlp = pipeline("sentiment-analysis", model=finbert, tokenizer=tokenizer)

def clean_text(text):
    """
    Cleans the text by removing unwanted characters and noise.
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs and email addresses
    text = re.sub(r'http\S+|www\S+|@\S+', '', text)
    
    # Remove HTML tags (if any)
    text = re.sub(r'<.*?>', '', text)
    
    # Remove non-alphabetical characters (keeping only letters and basic punctuation)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Remove extra whitespaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def calculate_polarity_scores(file_path, text_column, date_column, output_file):
    """
    Function to calculate polarity scores for each document in a CSV file, 
    handling long text by truncating it if needed to 512 tokens.
    """
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)
    
    # Create a new column to store the polarity result
    df['polarity'] = None  # Initialize empty polarity column
    df['score'] = None      # Initialize empty score column

    # Iterate through the dataframe and calculate sentiment for each row
    for index, row in df.iterrows():
        text = row[text_column]
        if pd.isna(text):
            continue

        # Clean the text before processing
        cleaned_text = clean_text(text)
        
        # Ensure text is encoded and truncated to stay within the 512 token limit
        result = nlp(cleaned_text, truncation=True, max_length=512)
        
        # Store the polarity label and score
        df.at[index, 'polarity'] = result[0]['label']
        df.at[index, 'score'] = result[0]['score']

    # Save the result back to a new CSV file
    df.to_csv(output_file, index=False)
    print(f"Polarity scores saved to {output_file}")

# Process each file with correct text and date columns
calculate_polarity_scores('./all_fed_speeches.csv', 'text', 'date', 'all_fed_speeches_with_polarity.csv')
calculate_polarity_scores('./df_minutes.csv', 'statements', 'Unnamed: 0', 'df_minutes_with_polarity.csv')
calculate_polarity_scores('./df_press_conferences.csv', 'press_conferences', 'Unnamed: 0', 'df_press_conferences_with_polarity.csv')
