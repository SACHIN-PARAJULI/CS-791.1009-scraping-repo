import os

# Directory containing the CSV files
directory = '/home/sudipnext/scraping/Audience/completed/'

# Old and new strings
old_str = 'top_critics'
new_str = 'audience'

# Loop through files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        # Generate the new filename
        new_filename = filename.replace(old_str, new_str)
        # Rename the file
        os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
