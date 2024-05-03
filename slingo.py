from argparse import ArgumentParser
import random

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

    def wildcard(self, wildcard_type):
        """Apply a wildcard effect to the game.

        Args:
            wildcard_type (str): The type of wildcard to apply.
        """
        if wildcard_type == "Double Points":
            #double the players points
            self.points *= 2
            print("Points Doubled!")
        if wildcard_type == "Remove Matches":
            for num in self.board.tiles:
                if num in self.player_board:
                    #remove matched number from the board
                    self.board.tiles.remove(num)
        if wildcard_type == "Free Space":
            random_num = random.choice(self.board.tiles)
            self.player_board.append(random_num)
            print("You have obtained a Free Space with number: ", random_num)
        if wildcard_type == "Lose Points":
            minimum = min(self.result)
            self.points -= minimum
            print(f"You lost {minimum} points.")

    def spin_wheel(self,special):
        """ This method "spins" the wheel, it generates either 5 random items, 
        these items can be 5 random digits or 4 random digits and 1 wildcard. 
        The function prints whatever items you "spin".

        Args:
            special (dict): A dictionary of lists describing the wildcards that 
            could be spun.

        Side effects:
            Prints to the player, the items that they rolled

        Returns:
            A list to the player that outlines what items they have rolled.
        """
        result = [random.randint(1,15),
              random.randint(16,30),
              random.randint(31,45),
              random.randint(46,60), 
              random.randint(61,75)]
        for slot in result:
            for character in special:
                chance = random.randint(1,100)
                if(chance <= special[character]):
                    index = result.index(slot)
                    result[index] = character
        return result
    
    def print_updated_board(self):
        """Prints the updated board with 'X' over the matched numbers in the player's board.
        """
        player_board_set = set(self.player_board)
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
        """Starts and plays the Slingo game.
        """
        print("Welcome to Slingo, let's begin!")
        print(f"Your starting balance: {STARTING_FUNDS}")

        while self.spins > 0:
            print("\nSpins left:", self.spins)
            print("Player board:", self.player_board)

            spin_result = self.spin_wheel(special_wildcards)
            self.spins -= 1

            # Update points earned
            points_earned = 0

            for item in spin_result:
                if isinstance(item, int) and item in self.player_board:
                    points_earned += 5
                    self.player_board[self.player_board.index(item)] = "X"
                elif isinstance(item, str) and item == "Free Space":
                    points_earned += 10

            self.player.add_points(points_earned)

            print("Spin Result:", spin_result)
            print("Points earned this round:", points_earned)
            print("Total points:", self.player.points)

            # Print the updated board
            self.print_updated_board()

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
        print (f"Welcome to Slingo {name}!")
        print (f"Your balance: {STARTING_FUNDS}")

        play = True
        while(play):
            response = input(f"Please select S to begin or select Q to quit: ")
            if response == "S" or response == "s":
                game = SlingoGame(player)
                game.board.printboard()

            elif response == "Q" or response == "q":
                print(f"Thank you for playing Slingo!")
                play = False
            
            else:
                print(f"Not a valid choice, please select S or Q.")
    
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
    main()
