import pandas as pd
import glob
import os

# Get a list of all CSV files in the current directory
csv_files = glob.glob('*.csv')

def convert_score(row):
    # Define a mapping from grades to ratios
    grade_to_ratio = {'A+': 1, 'A': 0.85, 'A-': 0.7, 'B+': 0.6, 'B': 0.5, 'B-': 0.4, 'C+': 0.3, 'C': 0.2, 'C-': 0.1, 'D': 0, 'F': 0}
    
    original_score = row['originalScore']
    sentiment = row['scoreSentiment']
    
    # Check if both columns are empty
    if pd.isna(original_score) and pd.isna(sentiment):
        return 'NEUTRAL'
    
    # Check if one column contains sentiment and the other is empty or non-numeric
    if (sentiment in ['POSITIVE', 'NEGATIVE'] and pd.isna(original_score)) or (original_score not in grade_to_ratio.keys() and pd.isna(original_score)):
        return sentiment
    
    # Check if one column contains a grade and the other is empty or non-sentiment
    if (original_score in grade_to_ratio.keys() and pd.isna(sentiment)) or (sentiment not in ['POSITIVE', 'NEGATIVE'] and pd.isna(sentiment)):
        return original_score
    
    # Check if one column contains a grade and the other contains a sentiment
    if original_score in grade_to_ratio.keys() and sentiment in ['POSITIVE', 'NEGATIVE']:
        if original_score == 'A+' and sentiment != 'POSITIVE':
            return 'POSITIVE'
        elif original_score == 'A-' and sentiment != 'NEGATIVE':
            return 'NEGATIVE'
        else:
            return sentiment
    
    # Check if one column contains a fraction and the other contains a sentiment
    if '/' in str(original_score) and sentiment in ['POSITIVE', 'NEGATIVE']:

        parts = original_score.split('/')
        if len(parts) != 2:
            return 'NEUTRAL'
        try:
            numerator, denominator = map(float, parts)
        except ValueError:
            return 'NEUTRAL'
        ratio = numerator / denominator
        if 0.4 <= ratio <= 0.6:
            return 'NEUTRAL'
        elif ratio > 0.6:
            return 'POSITIVE'
        else:
            return 'NEGATIVE'
    
    # Default case: return NEUTRAL
    return 'NEUTRAL'

for filename in csv_files:
    # Read the CSV file into a dataframe
    df = pd.read_csv(filename)
    
    # Rename 'creationDate' to 'Date'
    df.rename(columns={'creationDate': 'Date'}, inplace=True)
    
    # Drop the 'reviewUrl' column
    df.drop('reviewUrl', axis=1, inplace=True)
    
    # Merge 'originalScore' and 'scoreSentiment' into a single 'Score' column
    df['Score'] = df.apply(convert_score, axis=1)
    
    # Drop the original 'originalScore' and 'scoreSentiment' columns
    df.drop(['originalScore', 'scoreSentiment'], axis=1, inplace=True)
    
    # Save the processed dataframe to a new CSV file with the same name
    df.to_csv(f'processed/{filename}', index=False)
