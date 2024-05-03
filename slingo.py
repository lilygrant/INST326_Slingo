from argparse import ArgumentParser
import random
import sys

STARTING_FUNDS = 500
STARTING_SPINS = 15
#wildcard type and there chance (porbability) of showing up
special_wildcards = {"Double Points": 10, "Remove Matches": 5, "Free Space": 5, "Lose Points": 10}

class GameBoard():
    """Implements the game board.
    """
    def __init__(self):
        """Initializes the game board.
        """
        self.tiles = []

    def randomboard(self):
        """Generates the game board with randomly generated numbers.
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
        """
        b = self.tiles
        for row in range(5):
            print("----------------")
            print(
                "|" + str(b[row][0]) + 
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
        self.player = player
        self.board = GameBoard()
        self.board.randomboard()
        self.spins = STARTING_SPINS
        self.points = STARTING_FUNDS
        self.player_board = [] 
           


    def spin_wheel(self, special):
        """Spins the wheel and generates random items or wildcards."""
        result = []
        for _ in range(5):
            chance = random.randint(1, 100)
            random_num = random.randint(1, 75)  # Generate random number if no wildcard
            while random_num in result:  # Check for duplicates
                random_num = random.randint(1, 75)  # Generate a new random number
            if chance <= special_wildcards["Double Points"]:
                result.append("Double Points")
            elif chance <= special_wildcards["Double Points"] + special_wildcards["Remove Matches"]:
                result.append("Remove Matches")
            elif chance <= special_wildcards["Double Points"] + special_wildcards["Remove Matches"] + special_wildcards["Free Space"]:
                # When a "Free Space" wildcard is spun, ensure the number does not match any number in the spin result
                matched_numbers = [num for row in self.board.tiles for num in row]
                while random_num in matched_numbers or random_num in result:  # Check if the number already exists in the spin result
                    random_num = random.randint(1, 75)  # Generate a new random number
                result.append("Free Space")
                result.append(random_num)  # Add the random number
            elif chance <= special_wildcards["Double Points"] + special_wildcards["Remove Matches"] + special_wildcards["Free Space"] + special_wildcards["Lose Points"]:
                result.append("Lose Points")
            else:
                result.append(random_num)
        # Check for matches and add them to the player's board
        for item in result:
            if isinstance(item, int):
                for row in self.board.tiles:
                    if item in row:
                        self.player_board.append([item])  # Add matched number to player's board
                        row[row.index(item)] = 'X'  # Mark the number as matched on the game board
        return result





    def print_updated_board(self):
        """Prints the updated board with 'X' over the matched numbers in the player's board.
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
        
    def play_game(self):
        """Starts and plays the Slingo game."""
        
        print("Welcome to Slingo, let's begin!")
        print(f"Your starting balance: {STARTING_FUNDS}")
        
        while self.spins > 0:
            print("\nSpins left:", self.spins)
            print("Player board:", self.player_board)

            spin_result = self.spin_wheel(special_wildcards)
            self.spins -= 1

            # Update points earned
            points_earned = 0
            points_lost = 0
            
            for item in spin_result:
                if isinstance(item, int):
                    # Check if the number matches any on the board and update points earned
                    matched_numbers = []
                    for row in self.player_board:
                        if item in row:
                            points_earned += 5
                            matched_numbers.append(item)
                    if matched_numbers:
                        print("Matched numbers in this round:", matched_numbers)
                elif isinstance(item, str) and item == "Free Space":
                    # Implement logic to obtain a free space with a random number
                    random_num = spin_result[spin_result.index("Free Space") + 1]  # Get the next item after "Free Space"
                    self.player_board.append([random_num])
                    print("You have obtained a Free Space with number:", random_num)
                elif isinstance(item, str) and item == "Double Points":
                    print("Points Doubled!")
                elif isinstance(item, str) and item == "Lose Points":
                    # Implement logic to deduct points
                    points_to_lose = random.randint(1, 100)  # Example: random deduction between 1 and 100
                    if points_to_lose >= self.player.points:
                        # Points to lose exceed total points, end the game
                        print("You lost all your points. Game over!")
                        self.player.points = 0
                        break  # End the game
                    else:
                        points_lost += points_to_lose  # Accumulate points lost
                        print(f"You lost {points_to_lose} points.")
                                        
            if "Double Points" in spin_result:
                points_earned *= 2
                        
            # Calculate total points earned
            total_points_earned = points_earned - points_lost
            self.player.add_points(total_points_earned)

            print("Spin Result:", spin_result)
            print("Points earned this round:", total_points_earned)
            print("Total points:", self.player.points)

            # Print the updated board
            self.print_updated_board()
            
            while True:
                response = input("Press 's' to spin again or 'q' to exit: ")
                if response.lower() == 's':
                    break
                if response.lower() == 'q':
                    exit()

        print("No more spins left. Game over!")

    

class Player:
    """Represents the player in the game.
    """
    def __init__(self, name, points):
        """Initializes a Player instance.

        Args:
            name (str): The name of the player.
            points (int): The amonunt of points the player has.
        """
        self.name = name
        self.points = points

    def add_points(self, points):
        """Adds points to the player's total points.
        """
        self.points += points
        
            

    
#Main project file
def main():
    name = input("Please Enter your name: ")
    player = Player(name, STARTING_FUNDS)
    print(f"Welcome to Slingo {name}!")
    print(f"Your balance: {STARTING_FUNDS}")

    play = True
    while play:
        response = input("Please select S to begin or select Q to quit: ")
        if response.lower() == "s":
            game = SlingoGame(player)
            game.play_game()
        elif response.lower() == "q":
            print("Thank you for playing Slingo!")
            play = False
        else:
            print("Not a valid choice, please select S or Q.")

def parse_args(arglist):
    """Parse command-line arguments.

    Allow two optional arguments:
        -f, --funds: the starting funds for the player.
        -s, --spins: the starting spins for the player.

    Args:
        arglist (list of str): a list of command-line arguments.

    Returns:
        namespace: the parsed arguments, as a namespace.
    """
    parser = ArgumentParser()
    parser.add_argument("-f", "--funds", type=int, default=500, help="Starting funds for the player")
    parser.add_argument("-s", "--spins", type=int, default=15, help="Starting spins for the player")
    return parser.parse_args(arglist)

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    STARTING_FUNDS = args.funds
    STARTING_SPINS = args.spins
    main()