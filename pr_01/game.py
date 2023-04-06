#!/usr/bin/python
"""Script to create the box game"""

import numpy as np

class Board:
    """Class to generate and handle the board"""
    boardsize = (5, 5) # y x
    player_move = 1
    line_error = "Invalid line!"

    def __init__(self) -> None:
        self.gameboard = np.zeros(
            shape=self.boardsize,
            dtype=int
        )
        self.score = [0, 0]

    def play(self):
        """Function to run the game"""
        while True:
            self.print_board()

            user_input = self.validate_input(
                input(f"Player {self.player_move}, enter move 'y x line':")
            )

            if not user_input:
                continue

            bin_str = self.input_to_bits(user_input)
            points = 0

            match user_input[2]:
                # line:
                case 1:
                    # 0001 - DOWN   - 1
                    if (
                        user_input[0] == self.boardsize[0] - 1 or
                        bin_str[-1] == "1"
                    ):
                        print(self.line_error)
                        continue

                    self.gameboard[user_input[0]][user_input[1]] += 1
                    self.gameboard[user_input[0] + 1][user_input[1]] += 2

                    # Check down left
                    if (
                        bin_str[0] == "1" and (
                            self.input_to_bits([user_input[0] + 1, user_input[1] - 1])[2] == "1" and
                            self.input_to_bits([user_input[0] + 1, user_input[1] - 1])[1] == "1"
                        )
                    ):
                        points += 1

                    # Check down right
                    if (
                        bin_str[1] == "1" and (
                            self.input_to_bits([user_input[0] + 1, user_input[1] + 1])[2] == "1" and
                            self.input_to_bits([user_input[0] + 1, user_input[1] + 1])[0] == "1"
                        )
                    ):
                        points += 1

                case 2:
                    # 0010 - UP     - 2
                    if (
                        user_input[0] == 0 or
                        bin_str[-2] == "1"
                    ):
                        print(self.line_error)
                        continue

                    self.gameboard[user_input[0] - 1][user_input[1]] += 1
                    self.gameboard[user_input[0]][user_input[1]] += 2

                    # Check up left
                    if (
                        bin_str[0] == "1" and (
                            self.input_to_bits([user_input[0] - 1, user_input[1] - 1])[3] == "1" and
                            self.input_to_bits([user_input[0] - 1, user_input[1] - 1])[1] == "1"
                        )
                    ):
                        points += 1

                    # Check up right
                    if (
                        bin_str[1] == "1" and (
                            self.input_to_bits([user_input[0] - 1, user_input[1] + 1])[3] == "1" and
                            self.input_to_bits([user_input[0] - 1, user_input[1] + 1])[0] == "1"
                        )
                    ):
                        points += 1

                case 4:
                    # 0100 - RIGHT  - 4
                    if (
                        user_input[1] == self.boardsize[1] - 1 or
                        bin_str[-3] == "1"
                    ):
                        print(self.line_error)
                        continue

                    self.gameboard[user_input[0]][user_input[1]] += 4
                    self.gameboard[user_input[0]][user_input[1] + 1] += 8

                    # Check up right
                    if (
                        bin_str[2] == "1" and (
                            self.input_to_bits([user_input[0] - 1, user_input[1] + 1])[3] == "1" and
                            self.input_to_bits([user_input[0] - 1, user_input[1] + 1])[0] == "1"
                        )
                    ):
                        points += 1

                    # Check down right
                    if (
                        bin_str[3] == "1" and (
                            self.input_to_bits([user_input[0] + 1, user_input[1] + 1])[2] == "1" and
                            self.input_to_bits([user_input[0] + 1, user_input[1] + 1])[0] == "1"
                        )
                    ):
                        points += 1

                case 8:
                    # 1000 - LEFT   - 8
                    if (
                        user_input[1] == 0 or
                        bin_str[-4] == "1"
                    ):
                        print(self.line_error)
                        continue

                    self.gameboard[user_input[0]][user_input[1]] += 8
                    self.gameboard[user_input[0]][user_input[1] - 1] += 4
                    
                    # Check up left
                    if (
                        bin_str[2] == "1" and (
                            self.input_to_bits([user_input[0] - 1, user_input[1] - 1])[3] == "1" and
                            self.input_to_bits([user_input[0] - 1, user_input[1] - 1])[1] == "1"
                        )
                    ):
                        points += 1

                    # Check down left
                    if (
                        bin_str[3] == "1" and (
                            self.input_to_bits([user_input[0] + 1, user_input[1] - 1])[2] == "1" and
                            self.input_to_bits([user_input[0] + 1, user_input[1] - 1])[1] == "1"
                        )
                    ):
                        points += 1

            match points:
                case 0:
                    player_move = (self.player_move % 2) + 1
        
    def print_board(self):
        """Function to display the gameboard"""
        print()
        print(self.gameboard)
        print(f"Score:\nPlayer 1: {self.score[0]}\nPlayer 2: {self.score[1]}")

    def input_to_bits(self, user_input):
        """Convert the user inputed number to binary"""
        user_input = format(self.gameboard[user_input[0]][user_input[1]], 'b')

        while len(user_input) < 4:
            user_input = "0" + user_input

        return user_input

    def validate_input(self, player_input: str):
        """Validate user input"""
        x_location, y_location, line = player_input.split(" ")
        # line:
        # 0001 - Down   - 1
        # 0010 - Up     - 2
        # 0100 - RIGHT  - 4
        # 1000 - LEFT   - 8
        try:
            line = int(line)
            if line not in (1, 2, 4, 8):
                raise Exception(self.line_error)
        except Exception as exception_instance:
            print(exception_instance)
            return

        try:
            x_location = int(x_location)
            y_location = int(y_location)
            if not 0 <= x_location < self.boardsize[0]:
                raise Exception("Invalid x")
            if not 0 <= y_location < self.boardsize[1]:
                raise Exception("Invalid y")
        except Exception as exception_instance:
            print(exception_instance)
            return

        return (x_location, y_location, line)

if __name__ == "__main__":
    gamebord = Board()
    gamebord.play()
