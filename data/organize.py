import os
import shutil

# Function to group and rename files
def organize_movies(folder_path):
    # Iterate over each folder (audience and critics)
    for category in ['audience', 'critics']:
        category_path = os.path.join(folder_path, category)
        if not os.path.exists(category_path):
            continue

        # Iterate over each CSV file in the category folder
        for filename in os.listdir(category_path):
            if filename.endswith('.csv'):
                # Extract movie name from the filename
                movie_name = filename.replace('_' + category, '')

                # Convert the movie name to lowercase and replace spaces with underscores
                movie_name = movie_name.lower().replace(' ', '_')

                # Create a new folder for the movie if it doesn't exist
                movie_folder = os.path.join(folder_path, movie_name)
                if not os.path.exists(movie_folder):
                    os.makedirs(movie_folder)

                # Rename and move the file to the movie folder
                new_filename = f"{'a_' if category == 'audience' else 'c_'}{movie_name}.csv"
                shutil.move(os.path.join(category_path, filename), os.path.join(movie_folder, new_filename))

# Example usage
folder_path = ''
organize_movies(folder_path)
