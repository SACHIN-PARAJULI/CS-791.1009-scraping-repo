from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['TopMovies']  # Update with your actual database name
collection = db['test']  # Update with your actual collection name

# Define a function to search for emsId by movie name
def get_emsId_by_movie_name(movie_name):
    # Query MongoDB for the movie name
    result = collection.find_one({"movie_name": movie_name}, {"_id": 0, "emsId": 1})
    if result:
        return result.get('emsId')
    else:
        return None

# Example movie names
movie_names = [
    "Dune: Part Two",
    "Dune",
    "Oppenheimer",
    "Puss in Boots: The Last Wish",
    "Godzilla Minus One",
    "Marvel's The Avengers",
    "Mad Max: Fury Road",
    "The Lord of the Rings: The Two Towers",
    "Mission: Impossible - Fallout",
    "Captain America: Civil War",
    "Madame Web",
    "Best Laid Plans",
    "Gloria",
    "True Crime",
    "One Tough Cop",
    "Phoenix",
    "The Golden Child",
    "Imaginary",
    "Dreamland",
    "Rebel Moon: Part One - A Child of Fire",
    "Star Wars: The Last Jedi",
    "The Northman",
    "The Witcher",
    "The Lord of the Rings: The Rings of Power",
    "Indiana Jones and the Kingdom of the Crystal Skull",
    "The Witch",
    "The Eyes of My Mother",
    "Willow",
    "Uncut Gems",
    "Spy Kids",
    "Ant-Man and the Wasp: Quantumania",
    "Star Wars: the Rise of Skywalker",
    "Morbius",
    "Joker",
    "Man of Steel",
    "Eternals",
    "Godzilla: King of the Monsters",
    "Uncharted",
    "Fast X",
    "Warcraft"
]

# Loop through movie names and get emsId for each
movie_emsId_mapping = {}
for movie_name in movie_names:
    emsId = get_emsId_by_movie_name(movie_name)
    movie_emsId_mapping[movie_name] = emsId

# Print the mapping of movie names to emsId
for movie_name, emsId in movie_emsId_mapping.items():
    print(f"{movie_name}: {emsId}")
