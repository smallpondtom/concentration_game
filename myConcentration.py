"""
 ________   __________   ___________   ____________
|___  ___| |    ___   | |   ________| |            |
   |  |    |   |___|  | |   |         |   |    |   |
   |  |    |   _______| |   |         |   |    |   |
 __|  |    |   |        |   |_______  |   |    |   |
|_____|    |___|        |___________| |__ |___ |__ |

AUTHOR: TOMOKI KOIKE
"""

# Import necessary modules
import numpy as np
import random
import sys
from datetime import datetime


class ConcentrationGame:
    """
    Class of the game Concentration
    """

    def __init__(self):
        self.total_cards = 52  # total number of cards in deck
        self.state = self.shuffle_cards()  # shuffle the cards and line them up to initialize game
        self.computer_memory = {}  # empty dictionary for the computer's memory
        self.remaining = np.arange(self.total_cards)  # array indicating the remaining cards
        self.bin = []  # array to store cards that have been taken
        self.num = ['Ace'] + list(map(str, np.arange(2, 11))) + ['Jack', 'Queen', 'King']  # string with card numbers
        self.suits = ['diamonds', 'clubs', 'hearts', 'spades']  # string array with card suits
        self.deck = self.deck_dict()  # dictionary with all card names corresponding to card ID
        self.player_cards = 0  # number of cards that the player has
        self.computer_cards = 0  # number of cards that the computer has
        self.selected = [-1, -1]  # the temporary hold for the first choice of the player
        self.match = self.who_goes_first()  # 0 or 1 updated by whoever gets a match: 1 -> player and 0 -> computer

        """ 
        CARD IDs
        _______________________________________________________________________________________
        0 to 12 -> diamonds | 13 to 25 -> clubs   | 26 to 38 -> hearts  | 39 to 51 -> spades  
        0: Ace              | 13: Ace             | 26: Ace             | 39: Ace 
        1 to 9: 2 to 10     | 14 to 22: 2 to 10   | 27 to 35: 2 to 10   | 40 to 48: 2 to 10
        10: Jack            | 23: Jack            | 36: Jack            | 49: Jack
        11: Queen           | 24: Queen           | 37: Queen           | 50: Queen
        12: King            | 25: King            | 38: King            | 51: King
        _______________________________________________________________________________________
        """

    def deck_dict(self):
        """
        Function that creates the deck of cards as a dictionary
        :return: dictionary with the card number and suit {0: 'Ace of diamonds', 1: '2 of diamonds', ...}
        """

        deck = {}  # empty dictionary
        ct = 0  # initialize counter
        for suit in self.suits:
            for name in self.num:
                deck[ct] = name + ' of ' + suit
                ct += 1
        return deck

    def shuffle_cards(self):
        """
        This function initializes the shuffled cards to start playing the game
        :return: a 4x13 matrix with numbers from 0 to 51 shuffled randomly
        """

        cards = np.arange(self.total_cards)  # [0, 1, 2, ... 49, 50, 51]
        np.random.shuffle(cards)  # shuffle this
        initial_state = cards.reshape((4, int(self.total_cards / 4)))  # reshape this to 4x13
        return initial_state

    def play_game(self):
        """
        Function that plays the game (main function in the class)
        :return: none
        """

        print('Welcome to a game of Concentration!!')
        if self.who_goes_first():
            self.user_turn()
        else:
            self.computer_turn()

        while True:
            if self.match:
                self.user_turn()
            else:
                self.computer_turn()
            self.check_game_end()

    @staticmethod
    def who_goes_first():
        """
        Function that chooses who goes first 1 -> player and 0 -> computer
        :return: none
        """

        coin = random.choice([0, 1])  # flip a coin to decide who goes first
        return coin

    def check_game_end(self):
        """
        Function that determines whether the game is over or not by checking the remaining cards
        :return: none
        """

        if np.all(self.remaining == -1):  # end of game
            self.show_results()  # show the final results
            sys.exit()  # exit the program

    def show_results(self):
        """
        Function that shows the final results
        :return: none
        """

        if self.player_cards > self.computer_cards:  # player wins
            print('\nCongratulations!!')
            print('You WIN by {0} / {1}'.format(self.player_cards, self.computer_cards))
        elif self.player_cards < self.computer_cards:  # computer wins
            print('\nToo bad!!')
            print('You LOST by {0} / {1}'.format(self.player_cards, self.computer_cards))
        else:  # tied
            print('You TIED by {0} / {1}'.format(self.player_cards, self.computer_cards))

    def display_state(self):
        """
        Function that displays the current state of the game
        :return: none
        """

        print('\n')
        print('>>CURRENT STATE')
        ct = 0
        for i in self.state:
            for j in i:
                if j == -1:
                    val = 'X'
                else:
                    val = str(ct)
                if len(val) == 1:
                    print(' ' + val + ' ', end='')
                else:
                    print(val + ' ', end='')
                ct += 1
            print('\n')

    def input_validation(self, prompt):
        """
        Function that does the input validation for the user input
        :param prompt: the prompt used for the input
        :return: the input values (row, col)
        """

        while True:
            try:
                x, y = map(int, input(prompt).split())
            except ValueError:  # when there is less than or more than 2 input values
                print('Invalid input try again.')
                continue
            if (x != self.selected[0]) or (y != self.selected[1]):  # different from first choice
                if (0 <= x <= 3) and (0 <= y <= 12):  # Valid input
                    if not ([x, y] in self.bin):  # Check if this card is still there or not
                        break
                    else:
                        print('This card has already been taken.')
                        continue
                else:  # invalid input
                    print('Row and column should be from 0 to 3 and 1 to 12 respectively.')
                    continue
            else:
                print('Choose a card different from your first choice')
                continue
        return x, y

    def user_turn(self):
        """
        Function that operates the process for the player's turn
        :return: none
        """

        self.display_state()  # display the current state
        print(
            '\nTURN: You -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
        # Get the row and col number of the card you want to select
        x1, y1 = self.input_validation('Enter the location of the first card you pick (row, col) -> ')
        self.selected = [x1, y1]  # a temporary holder for the first choice

        # Get the corresponding card ID which is also the key for the dictionary with all the cards
        choice1_key = self.state[x1, y1]
        print('The card you selected: {0}'.format(self.deck[choice1_key]))

        # Repeat this for your second choice
        x2, y2 = self.input_validation('Enter the location of the second card you pick (row, col) -> ')
        self.selected = [-1, -1]  # reset the temporary hold

        choice2_key = self.state[x2, y2]
        print('The card you selected: {0}'.format(self.deck[choice2_key]))

        # Check if the two cards are a match or not
        if self.check_card(self.deck[choice1_key], self.deck[choice2_key]):
            print('MATCH')
            # Replace the corresponding cards in the remaining inventory and state with -1
            self.remaining[choice1_key] = -1
            self.remaining[choice2_key] = -1
            self.state[x1, y1] = -1
            self.state[x2, y2] = -1
            self.player_cards += 2  # the player gets 2 cards
            self.bin.append([x1, y1])  # move the location of the card to the already-taken bin
            self.bin.append([x2, y2])
            self.forget_memory(choice1_key)  # remove from computer's memory
            self.forget_memory(choice2_key)
            self.match = 1  # player will continue to choose cards
        else:
            print('NOT a match')
            # Add these cards to the computer's memory
            self.computer_memory[choice1_key] = [x1, y1]
            self.computer_memory[choice2_key] = [x2, y2]
            self.match = 0  # computer's turn

    def computer_turn(self):
        """
        Function that operates the process of the computer's turn
        :return: none
        """

        print(
            '\nTURN: Computer -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')

        # Scan through memory to see if the computer already knows a matching pair
        loc1, loc2 = self.computer_scan_memory()

        if loc1 and loc2:  # when there is a pair inside the computer's memory
            x1, y1 = loc1
            x2, y2 = loc2

            # Check point
            assert x1 != None and y1 != None, 'x1 or y1 is None type'
            assert x2 != None and y2 != None, 'x2 or y2 is None type'

            choice1_key = self.state[x1, y1]
            choice2_key = self.state[x2, y2]
        else:  # when there is no pair inside the computer's memory
            # Randomly select one card then scan memory
            x1, y1 = self.computer_random_select()
            choice1_key = self.state[x1, y1]

            # Scan through memory
            loc = self.computer_scan_memory(pick=choice1_key)

            if loc and (x1 != loc[0] or y1 != loc[1]):  # there is a common value card in the computer's memory
                x2, y2 = loc  # and that memory is not the same as the first choice

                # Check point
                assert x2 != None and y2 != None, 'x2 or y2 is None type'

                choice2_key = self.state[x2, y2]
            else:  # There is no common value in the computer's memory
                while True:  # select a card different from the first choice
                    x2, y2 = self.computer_random_select()
                    if x2 != x1 or y2 != y1:
                        break
                choice2_key = self.state[x2, y2]

        print('First choice: {0} ({1}, {2})'.format(self.deck[choice1_key], x1, y1))
        print('Second choice: {0} ({1}, {2})'.format(self.deck[choice2_key], x2, y2))

        # Check if it is a match or not
        if self.check_card(self.deck[choice1_key], self.deck[choice2_key]):
            print('MATCH')
            # Replace the corresponding cards in the remaining inventory and current state with -1
            self.remaining[choice1_key] = -1
            self.remaining[choice2_key] = -1
            self.state[x1, y1] = -1
            self.state[x2, y2] = -1
            self.computer_cards += 2  # the computer gets 2 cards
            self.bin.append([x1, y1])  # move the location of the card to the already-taken bin
            self.bin.append([x2, y2])
            self.forget_memory(choice1_key)  # remove from computer's memory
            self.forget_memory(choice2_key)
            self.match = 0  # The computer will continue to choose cards
        else:
            print('NOT a match')
            # Add these cards to the computer's memory
            self.computer_memory[choice1_key] = [x1, y1]
            self.computer_memory[choice2_key] = [x2, y2]
            self.match = 1  # The player's turn

    def computer_random_select(self):
        """
        Function that allows the computer to select a card randomly but quickly
        :return: the row and column index
        """

        while True:
            random.seed(datetime.now())  # generate a random seed using the current time to randomize selection in loop
            rand_row = random.sample([0, 1, 2, 3], 1)[0]  # sample a row number randomly

            # Check if the selected row has remaining cards
            row_in_state = self.state[rand_row, :]
            if not np.all(row_in_state < 0):  # NOTE: cards that are gone are indicated as -1
                break

        valid_col = np.where(row_in_state >= 0)[0]  # get the index of the cards that are still there
        choose_col = random.choice(valid_col)  # randomly select a column number within the cards that are still there
        return rand_row, choose_col

    def forget_memory(self, key):
        """
        Function that makes the computer forget a card in its memory
        :param key: the card ID
        :return: none
        """

        if key in list(self.computer_memory.keys()):
            del self.computer_memory[key]

    def computer_scan_memory(self, pick=None):
        """
        Function that scans through the computers memory to see if the computer knows cards with the same number
        :param: pick: if the computer has selected a card in advance this is the ID of the card chosen
        :return: the location the cards [x, y] or None
        """

        keys = np.asarray(list(self.computer_memory.keys()), dtype=int)
        keys_13 = np.mod(keys, 13)  # Take the modulus of 13 for all keys to see if there are any common numbers
        if pick == None:  # When there is no first choice
            if len(keys) >= 2:  # There has to be more than 2 memories
                for val in keys_13:  # Loop through all the key/card-ID modulo 13 values
                    # Get indices of common values (ID modulo of 13)
                    common_idx = list(filter(lambda x: keys_13[x] == val, range(len(keys_13))))
                    if len(common_idx) >= 2:  # If there are 2 or more common values
                        # Return the location [x, y] for common values inside memory
                        return self.computer_memory[keys[common_idx[0]]], self.computer_memory[keys[common_idx[1]]]
            return None, None  # If there are no common values return None
        else:  # When there is a first choice
            pick_13 = pick % 13  # take the modulus of the card-ID of the first choice
            # Get the indices of the common values (ID modulo of 13)
            common_idx = list(filter(lambda x: keys_13[x] == pick_13, range(len(keys_13))))
            if common_idx:  # if there was a common value to your first choice
                return self.computer_memory[keys[common_idx[0]]]
            return None  # if there was no common value to your first choice in the memory return None

    @staticmethod
    def check_card(card1, card2):
        """
        Function that checks if the two cards are a match or not
        :param card1: i.e. 'king of hearts'
        :param card2: i.e. '9 of clubs'
        :return: boolean if it is a match returns True and if not a match otherwise
        """

        num1 = card1.split(' ')[0]
        num2 = card2.split(' ')[0]

        if num1 == num2:
            return True
        else:
            return False


def main():
    shinkei_suijaku = ConcentrationGame()
    shinkei_suijaku.play_game()


if __name__ == '__main__':
    main()
