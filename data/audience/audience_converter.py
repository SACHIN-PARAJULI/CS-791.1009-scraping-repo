import pandas as pd
import glob
import os

# Get a list of all CSV files in the current directory
csv_files = glob.glob('*.csv')

def convert_score(row):
    # Check if the 'score' column exists in the row
    if 'score' in row:
        original_score = row['score']
        
        # Check if the score is empty
        if pd.isna(original_score):
            return 'NEUTRAL'
        
        # Check if the score is numeric
        if isinstance(original_score, (float, int)):
            # Map the score to a sentiment
            if original_score > 3.5:
                return 'POSITIVE'
            elif 2.5 < original_score <= 3.5:
                return 'NEUTRAL'
            elif original_score <= 2.5:
                return 'NEGATIVE'
    
    # Default case: return NEUTRAL
    return 'NEUTRAL'
for filename in csv_files:
    # Read the CSV file into a dataframe
    df = pd.read_csv(filename, on_bad_lines='skip')

    # Rename 'creationDate' to 'Date' and 'quote' to 'Review'
    df.rename(columns={'creationDate': 'Date', 'quote': 'Review'}, inplace=True)
    
    # Merge 'score' into a single 'Score' column
    df['Score'] = df.apply(convert_score, axis=1)
    
    # Select only 'Date', 'Review', and 'Score' columns
    df = df[['Date', 'Review', 'Score']]
    
    # Save the processed dataframe to a new CSV file with the same name
    df.to_csv(f'processed/{filename}', index=False)