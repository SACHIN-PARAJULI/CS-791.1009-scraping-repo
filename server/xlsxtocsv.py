# i want to convert a xlsx to csv file
import pandas as pd

def xlsx_to_csv(xlsx_file, csv_file):
    try:
        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(xlsx_file)
        
        # Write the DataFrame to a CSV file
        df.to_csv(csv_file, index=False)
        
        print(f"Conversion successful: {xlsx_file} -> {csv_file}")
    except Exception as e:
        print(f"Error converting {xlsx_file} to CSV:", e)

# Specify the input XLSX file and the output CSV file
xlsx_file = 'movies.xlsx'
csv_file = 'output.csv'

# Convert XLSX to CSV
xlsx_to_csv(xlsx_file, csv_file)
