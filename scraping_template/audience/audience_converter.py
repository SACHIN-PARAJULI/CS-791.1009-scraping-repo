import pandas as pd
import glob
import os

csv_files = glob.glob('*.csv')

def convert_score(row):
    if 'score' in row:
        original_score = row['score']
        
        if pd.isna(original_score):
            return 'NEUTRAL'
        
        if isinstance(original_score, (float, int)):
            # Map the score to a sentiment
            if original_score > 3.5:
                return 'POSITIVE'
            elif 2.5 < original_score <= 3.5:
                return 'NEUTRAL'
            elif original_score <= 2.5:
                return 'NEGATIVE'
    
    return 'NEUTRAL'

for filename in csv_files:
    df = pd.read_csv(filename, on_bad_lines='skip')
    df.rename(columns={'creationDate': 'Date', 'quote': 'Review'}, inplace=True)
    df['Score'] = df.apply(convert_score, axis=1)
    df = df[['Date', 'Review', 'Score']]
    df.to_csv(f'processed/{filename}', index=False)