from argparse import ArgumentParser
import random

#class that will implement the game board for the game Slingo
#we can initialize the board and display the board here 
class GameBoard():
    #game board is where the numbers are randomly generated or drawn during the game
    def __init__(self):
        """Initializes the game board.
        """
        self.tiles = []
    def checkBoard(self, player_board):
        """Checks the board for any complete rows, columns, or diagonals.

        Args:
            player_board (list of str): a 5x5 representation of the board, with randomly generated numbers
            for each tile and a free space in the middle.
        """
        size = 5
        checked_lines = 0
        for row in player_board:
            complete_row = True
            for num in row:
                if num not in self.tiles:
                    complete_row = False
                    break
            if complete_row:
                checked_lines += 1
        for col in range(size):
            complete_col = True
            for row in range(size):
                if player_board[row][col] not in self.tiles:
                    complete_col = False
                    break
            if complete_col:
                checked_lines += 1
        complete_d1 = True
        complete_d2 = True
        for diag in range(size):
            if player_board[diag][diag] not in self.tiles:
                    complete_d1 = False
                    break
            if player_board[diag][diag] not in self.tiles:
                    complete_d2 = False
                    break
            if complete_d1:
                checked_lines += 1
            if complete_d2:
                checked_lines += 1
        if checked_lines > 0:
            print("Slingo!")
        
class SlingoGame:
    def __init__(self):
        self.points = 0
        self.board = GameBoard()

        # specific to each player and represents the card or grid of numbers 
        # that the player is trying to match with the numbers drawn from the game board.
        self.player_board = []       

    def placeBet(self, bet): 
        pass

    def wildcard(self,wildcard_type):
        if wildcard_type == "Double Points":
            #double the players points
            self.points *= 2
            print("Points Doubled!")
        if wildcard_type == "Remove Matches":
            for num in self.board.tiles:
                if num in self.player_board:
                    #remove matched number from the board
                    self.board.tiles.remove(num)
class Player:
    def __init__(self, name, funds):
        self.name = name
        self.funds = funds
        #starting balance of player
        
    def placeBet(self, bet): 
        if bet > self.funds:
            print(f'Not enough funds')
            #bets cannot exceed funds
        else:
            self.funds -= bet
            return bet 
            #reduced funds after placed bet
            

def spin_wheel(special):
    """ This function "spins" the wheel, it generates either 5 random items, 
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
    
#Main project file
def main():
    test = {
    "WILD": 2,
    "JOKE": 2,
    "X2": 2
    }
    print(spin_wheel(test))
    
#Parse command-line arguments.
def parse_args(arglist):
    parser = ArgumentParser()
    return parser.parse_args(argslist)
main()
