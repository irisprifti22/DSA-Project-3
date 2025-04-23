
# GameMatcher: A Personalized Video Game Recommendation System

 ## Team Members: Iris Prifti, Adiel Garcia Tavarez, Alex Yan (Group 54)
 
 Players often feel overwhelmed when choosing a new game from an ever expanding market, resulting in time consuming searches, frustrating purchases and unnecessary spending.

Our project, GameMatcher, tackles this problem by using a balanced red-black tree and a hash table for genre and developer mapping, then weighting candidates by review similarity and other key metrics to produce a concise, ranked list of tailored suggestions.

Our solution serves avid gamers who want a quicker, more personal way to discover titles and it helps developers and publishers engage the right audiences and optimize their marketing efforts.


## Features

- Welcome screen with team information and a start button

- Home screen offering two intuitive search modes

- Search by Title uses a djb2 hash table to lookup games and a weighted relevance formula to recommend the top ten matches

- Search by Genre uses a Red-Black Tree to index all games by title and returns the first ten entries for a selected genre

- Data loading from CSV with pandas, including handling of missing or malformed fields using average ratings and default playtime

- Customizable fonts and a background image for a polished, consistent UI

## Installation

What you will need to run our program:

- Python 3.7 or newer, with tkinter installed

- pandas (pip install pandas)

- Pillow (pip install pillow)

- game_info.csv placed in the project root
    
From the project root, execute: python WelcomeWindow.py

Click Click to Start to open the main screen, select Search by Title or Search by Genre, enter your query, then click Search to view personalized recommendations.
## Architecture and Strategy
Title Lookup: djb2 hash table with separate chaining for O(1) average retrieval

Genre Indexing: Red-Black Tree ensures balanced insertions and quick in-order traversals

Recommendation Logic: heapq max-heap selects top matches using a relevance score based on normalized metacritic, playtime ratio, shared platforms, developers, publishers, and genres
## File Structure

GameMatcher/

├── resources/

│   └── images/

│       └── welcomeWindowBackground.jpg

├── game_info.csv

├── WelcomeWindow.py

├── HomeScreen.py

├── SearchName.py

├── SearchGenre.py

├── hashtable.py

├── red_black_tree.py

└── README.md
## Group Members

- [Iris Prifti](https://github.com/AlexYan8)
- [Adiel Garcia Tavarez](https://github.com/AlexYan8)
- [Alex Yan](https://github.com/AlexYan8)



## Sources

 - [Hashmaps in Python](https://stackoverflow.com/questions/8703496/hash-map-in-python)
 - [Hashmap Guide](https://www.analyticsvidhya.com/blog/2024/06/python-hashmaps/)
 - [Red and Black Trees in Python](https://www.geeksforgeeks.org/red-black-tree-in-python/)


## Troubleshooting
- If Calisto MT isn’t available, the default system font will be used

- Missing game_info.csv or malformed entries may cause errors—ensure it’s in the root and correctly delimited