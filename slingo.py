from argparse import ArgumentParser
import random
import sys
import seaborn as sns
import matplotlib.pyplot as plt
import re
import json
import csv
import pandas as pd
import os

STARTING_SPINS = 10
#Wildcard type and their chance (probability) of showing up.
special_wildcards = {"Double Points": 3,  "Free Space": 5, "Lose Points": 3}

class GameBoard():
    """Implements the game board. 
    """
    def __init__(self):
        """Initializes the game board.
        
        Author: Egypt Butler 
        """
        self.tiles = []

    def randomboard(self):
        """Generates the game board with randomly generated numbers.
    
        Returns:
            tiles (list): The numbers within the Gameboard tiles.
        
        Side effects:
            Appends values used to the 'used' and 'row' lists to keep track of 
            values used in the random board. 
            
        Author: Lily Grant 
        """

        tiles = []
        used = []
        for column in range(5):
            row = []
            num = random.randint(1,15)
            while (num in used):
                num = random.randint(1,15)
            row.append(num)
            used.append(num)

            num = random.randint(16,30)
            while (num in used):
                num = random.randint(16,30)
            row.append(num)
            used.append(num)

            num = random.randint(31,45)
            while (num in used):
                num = random.randint(31,45)
            row.append(num)
            used.append(num)

            num = random.randint(46,60)
            while (num in used):
                num = random.randint(46,60)
            row.append(num)
            used.append(num)

            num = random.randint(61,75)
            while (num in used):
                num = random.randint(61,75)
            row.append(num)
            used.append(num)

            tiles.append(row)
        self.tiles =  tiles

    def printboard(self):
        """Displays the game board.

        Side effects:
            Prints the randomly generated numbers generated for the Gameboard
            in their own boxes. 
            
        Author: Lily Grant 
        """
        b = self.tiles
        for row in range(5):
            x = ""
            print(b[row][0])
            if int(b[row][0]) < 10:
                x = str(b[row][0]+ " ")
            else:
                x = str(b[row][0])
            print("----------------")
            print(
                "|" + x + 
                "|" + str(b[row][1]) + 
                "|"+ str(b[row][2]) + 
                "|" + str(b[row][3]) + 
                "|" + str(b[row][4]) + 
                "|")
            print("----------------")

    def checkBoard(self, player_board):
        """Checks the board for any complete rows, columns, or diagonals. 

        Args:
            player_board (list of str): a 5x5 representation of the board, with randomly generated numbers
            for each tile and a free space in the middle.
        
        Returns:
            boolean: True if there is a complete row, column, or diagonal.

        Author: Maggie Zhang
        """
        #Defines all groups where a win is possible.
        complete = [(0, 1, 2, 3, 4), (5, 6, 7, 8, 9), (10, 11, 12, 13, 14),
                 (15, 16, 17, 18, 19), (20, 21, 22, 23, 24), (0, 5, 10, 15, 20),
                 (1, 6, 11, 16, 21), (2, 7, 12, 17, 22), (3, 8, 13, 18, 23),
                 (4, 9, 14, 19, 24), (0, 6, 12, 18, 24), (4, 8, 12, 16, 20)]
        for spots in complete:
            complete_line = True
            for index in spots:
                if player_board[index] != "X":
                    complete_line = False
                    break
            if complete_line:
                return True
        return False
        
class SlingoGame:
    """Implements the game of Slingo.
    """
    def __init__(self, player):
        """Initializes a SlingoGame instance.

        Args:
            player (Player): The player participating in the game.

        Side Effects:
            - Initializes the game state including the player, game board, spins, player board, and scores.
            
        Author: Egypt Butler 
        """
        self.player = player
        self.board = GameBoard()
        self.board.randomboard()
        self.spins = STARTING_SPINS
        self.player_board = [] 
        self.scores = []
    
    def __repr__(self):
        """ Provides a formal string representation of the SlingoGame class.

        Returns:
            F string: containing information on the state of the game like the 
            player's name and number of spins. 
            
        Author: Lily Grant

        Technique: magic methods
        """
        return f"SlingoGame({self.player}, {self.spins})"

    def spin_wheel(self,special):
        """Spins the wheel and generates random items or wildcards.
        
        Args:
            special (dict): a dictionary of types of wildcards you can roll as 
            keys and their values are their point values.
            
        Returns:
            result(list of integers or str): The numbers or wildcards that the 
            player has spun for the given turn.
            
        Side effects:
            Alters the tiles within the class and replaces them with an 'X' when 
            a value matches an original number in a tile. 
            
        Author: Lily Grant
        
        """
        result = []
        for _ in range(5):
            chance = random.randint(1, 100)
            random_num = random.randint(1, 75)  

            while random_num in result:
                random_num = random.randint(1, 75) 

            if chance <= special_wildcards["Double Points"]:
                result.append("Double Points")

            elif chance <= special_wildcards["Double Points"] + special_wildcards["Free Space"]:
                matched_numbers = [num for row in self.board.tiles for num in row]

                while random_num in matched_numbers or random_num in result: 
                    random_num = random.randint(1, 75)  
                result.append(random_num) 

            elif chance <= special_wildcards["Double Points"] + special_wildcards["Free Space"] + special_wildcards["Lose Points"]:
                result.append("Lose Points")
            else:
                result.append(random_num)

        # Check for matches and add them to the player's board
        for item in result:
            if isinstance(item, int):
                for row in self.board.tiles:
                    if item in row:
                        self.player_board.append([item])  
                        row[row.index(item)] = 'X ' 
        return result


    def print_updated_board(self):
        """Prints the updated board with 'X' over the matched numbers in the 
            player's board.
        
        Side Effects:
            Prints the updated game board to the console.
            
        Author: Egypt Butler 
        """
        player_board_set = set(map(tuple, self.player_board))
        for row in range(5):
            print("----------------")
            for col in range(5):
                num = self.board.tiles[row][col]
                if num in player_board_set:
                    print("|X", end="")
                else:
                    print(f"|{num}", end="")
            print("|")
        print("----------------")

    def max_contribution(self, spin_scores):
        """Prints the spin that contributed the most points. 
        
        Args:
            spin_scores (list): List of scores obtained in each spin.

        Author: Maggie Zhang
        
        Technique: Use of a key function with max()
        """
        if spin_scores:
            max_contribution = max(spin_scores, key=lambda x: x)
            print(f"The spin that contributed the most points was {max_contribution}.")
    
    def play_game(self, special_wildcards = None):
        """Starts and plays the Slingo game.

        Args:
            special_wildcards (dict, optional): A dictionary containing special wildcards and their probabilities.

        Side Effects:
            - Manages the game loop, including player spins, updating points, and printing game information.
            - Modifies the game state including player points, spins left, and player board.
            
        Author: Egypt Butler
        
        Technique: Optional Parameters 
        """
        
        print("Welcome to Slingo, let's begin!")
        print("Here is your Slingo board: ")
        self.print_updated_board()
        spin_scores = []
        while self.spins > 0:
            print("\nSpins left:", self.spins)
            print("Player board:", self.player_board)

            spin_result = self.spin_wheel(special_wildcards)
            self.spins -= 1

            # Update points earned
            points_earned = 0
            points_lost = 0
            
            total_points_earned = points_earned - points_lost
            self.player.add_points(total_points_earned)
            self.scores.append(self.player.points) 
       
            
            for item in spin_result:
                if isinstance(item, int):
                    matched_numbers = []

                    for row in self.player_board:
                        if item in row:
                            points_earned += 5
                            matched_numbers.append(item)

                    if matched_numbers:
                        print("Matched numbers in this round:", matched_numbers)

                elif isinstance(item, str) and item == "Free Space":
                    random_num = spin_result[spin_result.index("Free Space") + 1]  
                    self.player_board.append([random_num])
                    print("You have obtained a Free Space with number:", random_num)

                elif isinstance(item, str) and item == "Double Points":
                    print("Points Doubled!")

                elif isinstance(item, str) and item == "Lose Points":
                    points_to_lose = random.randint(1, 50)  

                    if points_to_lose >= self.player.points:
                        print("You lost all your points. Game over!")
                        self.player.points = 0
                        break  
                    else:
                        points_lost += points_to_lose  # Accumulate points lost
                        print(f"You lost {points_to_lose} points.")
                                        
            if "Double Points" in spin_result:
                points_earned *= 2
                        
            # Calculate total points earned
            total_points_earned = points_earned - points_lost
            self.player.add_points(total_points_earned)
            spin_scores.append(total_points_earned)

            print("Spin Result:", spin_result)
            print("Points earned this round:", total_points_earned)
            print("Total points:", self.player.points)

            
            self.print_updated_board()

            if self.player.points >= 200:
                print("Game over! You have reached or exceeded 200 points! Select 'q' to quit and see stats")
                self.max_contribution(spin_scores)
                return
            
            while True:
                response = input("Press 's' to spin again or 'q' to exit: ")
                if response.lower() == 's':
                    break
                if response.lower() == 'q':
                    exit()

        print("No more spins left. Game over!")
        self.max_contribution(spin_scores)
    
    def save_game_state(self, filename):
        """it saves the current game state to a JSOnfile.
        
        Args: 
        filename (str): name of file to save data
        """
        
        game_state = {
            "player_name": self.player.name,
            "points": self.player.points,
            "board":self.player_board,
            "spins": self.spins,
            "scores":self.scores
        }
        with open(filename, "w") as f:
            json.dump(game_state, f)
    
    def curr_game_state(self, filename):
        """Load the game state from a JSON file.

        Args:
            filename (str): The name of the JSON file containing the game state.

        Author: Nahum Ephrem

        Technique: JSON.load()
        """
        with open(filename, "r") as f:
            game_state = json.load(f)
            self.player.name = game_state["player_name"]
            self.player.points = game_state["points"]
            self.player_board = game_state["board"]
            self.spins = game_state["spins"]
            self.scores = game_state["scores"]


class Player:
    """Represents the player in the game.
    """
    def __init__(self, name, points):
        """Initializes a Player instance.

        Args:
            name (str): The name of the player.
            points (int): The amonunt of points the player has.
            
        Author: Egypt Butler
        
        Technique: Regular Expressions
        """
        if not re.match(r"^[a-zA-Z\s]+$", name):
            raise ValueError("Invalid name. Name must contain only letters and spaces.")
        self.name = name
        self.points = points

    def __repr__(self):
        """String representation of Player instance.
        
        Author: Lily Grant

        Technique: magic methods
        """
        return f"Player({self.player}, {self.points})"

    def add_points(self, points):
        """
        Adds points to the player's total points. Egypt Butler is the primary
        author.

        Args:
            points (int): The number of points to add to the player's total points.

        Side Effects:
            Modifies the player's total points.
            
        Author: Egypt Butler
        """
        self.points += points
         
def plot_score_trend(scores_all_games):
    """Plot the trend of winners scores(at least 200 pt) over multiple games. 

    Args:
        scores_all_games (list of int): List of scores after each game.

    Author: Nahum Ephrem

    Technique: Visualizing data (pyplot and seaborn)
    """
    plt.figure(figsize=(12, 6))
    sns.lineplot(x=range(1, len(scores_all_games)+1), y=scores_all_games)
    plt.xlabel('Spin Number')
    plt.ylabel('Score')
    plt.title('Winner (200pt) Score Trend Over Multiple Spins')
    plt.show()
    
def create_csv_when_quit(scores_all_games):
    """Create a CSV file when the player clicks 'q' to quit the game.

    Args:
        scores_all_games (list of int): List of scores after each game.

    Returns:
        bool: True if a CSV file was created, False otherwise.

    Author: Nahum Ephrem
    """
    if scores_all_games:
        with open('scores_when_quit.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Spin', 'Score'])
            for i, score in enumerate(scores_all_games, start=1):
                writer.writerow([i, score])
        print("Scores saved successfully.")
        return True
    print("No scores to save.")
    return False



def filter_best_spins(scores_filename, output_filename):
    """Filter the best spins that earned above the average increase.

    Args:
        scores_filename (str): The name of the input CSV file containing scores.
        output_filename (str): The name of the output CSV file to save the filtered spins.

    Author: Nahum Ephrem
    Technique: Pandas
    """
    if not os.path.exists(scores_filename):
        print(f"File {scores_filename} does not exist. Exiting filtering process.")
        return None

    df = pd.read_csv(scores_filename)
    df['Score Increase'] = df['Score'].diff().fillna(0)
    top_spins = df.sort_values(by='Score Increase', ascending=False).head(10)
    top_spins.to_csv(output_filename, index=False)
    print(f"Filtered data saved to {output_filename}, Win at 200 points for graph.")



#Main project file
def main():
    """ This functions runs the game of slingo and works by prompting the player
        a set of questions.
         
        Side effects:
            prints to the player their options for the game. 
            intializes the SlingoGame class and Player class.
            prints the file line by line if the player requests help.
            plots the score trend for the player

        Returns:
            The score of the game.
            
        Author: Lily Grant

        Technique: with statement 
        Technique: F strings containing expressions
          """
    name = input("Please Enter your name: ")
    player = Player(name,0)
    game = SlingoGame(player)
    game.play_game()
    print(f"Welcome to Slingo {name}!")
    
    if create_csv_when_quit(game.scores):
        filter_best_spins('scores_when_quit.csv', 'top_10_spins.csv')
    else:
        print("No data to generate CSV.")

    play = True
    scores_all_games = []  # Store score from all games
    while play:
        response = input("Please select s to begin, select q to quit, or select h for help: ")
        if response.lower() == "s":
            game = SlingoGame(player)
            game.play_game()
            scores_all_games.extend(game.scores)  # Adds scores from the current game to the list
        elif response.lower() == "q":
            print("Thank you for playing Slingo!")
            plot_score_trend(scores_all_games)
            if create_csv_when_quit(scores_all_games):
                filter_best_spins('scores_when_quit.csv', 'top_10_spins.csv')
            play = False
        elif response.lower() == "h":
            with open("Slingo_example.txt", "r", encoding= "utf-8") as f:
                for line in f:
                    print(line)
        else:
            print(f'Not a valid choice, please select s, h, or q.')
    
      # plots the score trend after all games have been played

 # Save game state
    game.save_game_state("game_state.json")

    # Load game state
    game.curr_game_state("game_state.json")



def parse_args(arglist):
    """Parse command-line arguments. 

    Allow one optional argument:
        -s, --spins: the starting spins for the player.

    Args:
        arglist (list of str): a list of command-line arguments.

    Returns:
        namespace: the parsed arguments, as a namespace.

    Author: Maggie Zhang

    Technique: Argument Parser 
    """
    parser = ArgumentParser()
    parser.add_argument("-s", "--spins", type=int, default=10, help="Starting spins for the player")
    return parser.parse_args(arglist)

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    STARTING_SPINS = args.spins
    main()
