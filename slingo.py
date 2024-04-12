from argparse import ArgumentParser

#class that will implement the game board for the game Slingo
#we can initialize the board and display the board here 
class GameBoard():
    #game board is where the numbers are randomly generated or drawn during the game
    def __init__(self):
        self.tiles = [] #
        
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
                
            
    
#Main project file
def main():
    print("hello world")
    print("added this code")
    
#Parse command-line arguments.
def parse_args(arglist):
    parser = ArgumentParser()
    return parser.parse_args(argslist)

