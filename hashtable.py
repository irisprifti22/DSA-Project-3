import csv
import pandas

class GameManager:
    # Nested class to represent a game
    # This class stores information about a game necessary to calculate relevancy scores between games

    class Game:
        def __init__(self, title, metacritic, playtime, platforms, genres, publishers, developers):
            self.title = title
            self.metacritic = metacritic
            self.playtime = playtime
            self.platforms = platforms
            self.genres = genres
            self.publishers = publishers
            self.developers = developers

        def print(self):
            # Print the game information
            print(f"Title: {self.title}")
            print(f"Metacritic: {self.metacritic}")
            print(f"Playtime: {self.playtime}")
            print(f"Platforms: {', '.join(self.platforms)}")
            print(f"Genres: {', '.join(self.genres)}")
            print(f"Publishers: {', '.join(self.publishers)}")
            print(f"Developers: {', '.join(self.developers)}")

    def __init__(self, size=632581):
        # Initialize size to the next prime number after the number of entries divided by 0.75 (our ideal load factor)
        self.size = size
        # Initialize the hash table with empty lists for separate chaining
        self.table = [[] for i in range(size)]

    def djb2(self, key):
        # Standard djb2 hash function
        hash = 5381
        for c in key:
            hash = ((hash << 5) + hash) + ord(c)
        return hash
    
    def hash(self, key):
        # Hash the key using the djb2 function and reduce
        return self.djb2(key) % self.size

    def read(self):
        # Read the data from the csv file
        file = pandas.read_csv('game_info.csv')

        # Calculate the average rating to apply to games without one so that they are not judged unfairly
        average_rating = file["metacritic"].mean(skipna=True)

        for index, row in file.iterrows():
            # During testing, found several errors being caused by erroneous titles
            # Check all titles for NaN, empty values, and empty space, and nonstring data types
            title = row['name'].strip() if pandas.notna(row['name']) else None
            # If the title is invalid, move on
            if not title:
                continue

            meta_raw = row['metacritic']
            play_raw = row['playtime']

            # Handle NaN and empty values
            metacritic = float(meta_raw) if pandas.notna(meta_raw) else average_rating
            playtime = int(play_raw) if pandas.notna(play_raw) else 0

            # Separate list items by their delimiter, ||
            # Make sure to handle NaN and empty values
            platforms = row['platforms'].split('||') if pandas.notna(row['platforms']) else []
            genres = row['genres'].split('||') if pandas.notna(row['genres']) else []
            publishers = row['publishers'].split('||') if pandas.notna(row['publishers']) else []
            developers = row['developers'].split('||') if pandas.notna(row['developers']) else []

            # Create a new game object
            game = self.Game(title, metacritic, playtime, platforms, genres, publishers, developers)

            # Hash the game title to generate an index
            index = self.hash(title)

            # Insert the game into the hash table
            # No need to check for duplicates, as the input file contains none
            self.table[index].append((title, game))

    def get(self, key):
        # Get the index based on the key, which is the title of the game
        index = self.hash(key)
        # Check if the index is empty
        if self.table[index] is not None:
            # Iterate through the list at that index
            for pair in self.table[index]:
                # If the key matches, return the value
                if pair[0] == key:
                    return pair[1]