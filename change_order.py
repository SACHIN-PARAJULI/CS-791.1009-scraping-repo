import pandas as pd
import glob
import os

# Function to modify CSV files
def modify_csv_files(folder_path):
    print(f"Modifying CSV files in folder: {folder_path}")

    # Iterate over each CSV file in the folder and its subfolders
    for filename in glob.glob(os.path.join(folder_path, '**/*.csv'), recursive=True):
        print(f"Processing file: {filename}")

        # Load the CSV file
        df = pd.read_csv(filename)

        # Rename the columns
        df.columns = ['Date', 'Reviews', 'Score']

        # Remove the quotes from the Date column
        df['Date'] = df['Date'].str.replace('"', '')

        # Reorder the columns
        df = df.reindex(columns=['Date', 'Score', 'Reviews'])

        # Save the modified DataFrame back to the CSV file
        df.to_csv(filename, index=False)
        print(f"Modified file: {filename}")

# Call the function after organizing the movies
folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data copy')
modify_csv_files(folder_path)