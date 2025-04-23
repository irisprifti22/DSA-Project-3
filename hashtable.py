from math import log
import pandas
import heapq

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

    genre_map = {}

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

            # Insert the game into its corresponing genre list in the dictionary 
            # If its genre is not in the map, create a new list
            for genre in genres:
                if genre not in self.genre_map:
                    self.genre_map[genre] = []
                self.genre_map[genre].append(game)


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
                
    def relevance(self, key1, key2):
        # Get both games from the hash table
        game1 = self.get(key1)
        game2 = self.get(key2)

        # Get necessary values
        # Normalize metacritic score
        meta = game2.metacritic/100

        # Use a logarithmic ratio to calculate how playtime will affect the score
        # The closer the playtimes, the higher the score
        # Normalize the playtime score by dividning by the supposed max of 120
        # Check first if either if is 0
        # Apparently playtime can be negative, because some of the log operations were returning complex numbers
        # which implies that the playtime was negative, so if it is, set it to 0
        if game1.playtime <= 0 or game2.playtime <= 0:
            play = 0
        else:
            play = 1 - log(max(game1.playtime, game2.playtime) / min(game1.playtime, game2.playtime)) / log(120)

        # Platform, developer, and publisher scores are 1 if games share a platform, 0 if not
        plat = 1 if set(game1.platforms) & set(game2.platforms) else 0
        dev = 1 if set(game1.developers) & set(game2.developers) else 0
        pub = 1 if set(game1.publishers) & set(game2.publishers) else 0

        # Calculate genre similarity based on how many genres are shared
        gen = len(set(game1.genres) & set(game2.genres))
        # Normalize the genre score by dividing by the genre cap, which is 3, so that other attributes still have weight
        gen = min(gen, 3) / 3

        # Put all the scores into a formula with their respective weights
        # Weights were calculated based on relative importance
        result = (2.4 * meta) + (0.55 * play) + (2.0 * plat) + (1.4 * dev) + (0.9 * pub) + (0.8 * gen)

        # Return the result
        return result

                
    # Pull recommendations based on the game title
    # Recommendations will be based on a formula that assigns different weights to each attribute of each game
    # of the same genre as the game being searched for
    def get_recommendations_by_title(self, key):
        # Store the games' genres
        genres = self.get(key).genres

        # Get the list of games in the same genres. Store them in a priority queue
        # Create a set to check for duplicates
        seen = set()
        # Create a priority queue to store the games
        matches = []

        for genre in genres:
            # Iterate through list of games in each genre
            for game in self.genre_map[genre]:
                # Skip the game being searched for
                if game.title == key:
                    continue
                # Check if the game has been seen before
                if game.title not in seen:
                    seen.add(game.title)
                    # Calculate the relevance score
                    score = self.relevance(key, game.title)
                    # Push the game into the priority queue with the score as its priority
                    # Negate the score to make it a max heap
                    # Use the title as a tiebreaker in case they have the same score
                    heapq.heappush(matches, (-score, game.title, game))
        
        # Get the top 10 games
        recommendations = []
        for i in range(10):
            # Check that there are still games in the priority queue
            if matches:
                # Pop the game, which is in the 3rd position in the tuple
                recommendations.append(heapq.heappop(matches)[2])
            else:
                break

        # Return the recommendations as tuples with all the info needed by the UI
        return [(game.title, game.genres, game.developers, game.platforms) for game in recommendations]
        
    def get_recommendations_by_genre(self, key):
        # Get the top 10 games from the genre in the genre map
        recommendations = []
        for i in range(10):
            # Check that there are still games in the genre map
            if key in self.genre_map and i < len(self.genre_map[key]):
                recommendations.append(self.genre_map[key][i])
            else:
                break
        
        # Return the recommendations as tuples with all the info needed by the UI
        return [(game.title, game.genres, game.developers, game.platforms) for game in recommendations]