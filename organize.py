import os
import shutil

# Function to group and rename files
def organize_movies(folder_path):
    print(f"Folder path: {folder_path}")

    # Iterate over each folder (audience and critics)
    for category in ['audience/processed', 'critics/processed']:
        print(f"Processing category: {category}")
        category_path = os.path.join(folder_path, category)
        if not os.path.exists(category_path):
            print(f"Category path not found: {category_path}")
            continue

        # Iterate over each CSV file in the category folder
        for filename in os.listdir(category_path):
            if filename.endswith('.csv'):
                # Extract movie name from the filename
                movie_name = filename.replace('_' + category.split('/')[0], '').replace('.csv', '')
                print(f"Processing file: {filename}, movie name: {movie_name}")

                # Convert the movie name to lowercase and replace spaces with underscores
                movie_name = movie_name.lower().replace(' ', '_')

                # Create a new folder for the movie if it doesn't exist
                movie_folder = os.path.join(folder_path, movie_name)
                if not os.path.exists(movie_folder):
                    os.makedirs(movie_folder)

                # Rename and move the file to the movie folder
                new_filename = f"{'a_' if 'audience' in category else 'c_'}{movie_name}.csv"
                shutil.move(os.path.join(category_path, filename), os.path.join(movie_folder, new_filename))
                print(f"Moved file to: {os.path.join(movie_folder, new_filename)}")

# Example usage
folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data copy')
organize_movies(folder_path)