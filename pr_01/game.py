#!/bin/python3
"""Script to create the box game"""

import logging
import sys
import json
import timeit
import math
import time

import tkinter as tk
import numpy as np

class GameBoard:
    """Class to manage the line game"""

    def __init__(self, size) -> None:
        """Constructor to set the start values"""

        # Setting empty values
        self.window_frame = None
        self.selected_button = None
        self.player_move = None
        self.boardsize = None
        self.gameboard = None
        self.button_canvas = None
        self.line_set = None
        self.tree = None

        self.window = tk.Tk()
        self.reset(size)
        self.full_tree = self.generate_gametree(
            # filename = "gametree.json",
            # depth=2
        )
        self.tree = self.full_tree
        
    def wait_move(self):
        logging.debug("Waiting for move...")
        if self.player_move == 2:
            self.computer_move()
        elif self.player_move == 1:
            logging.info("Player move")

    def computer_move(self):
        if len(self.line_set) == 0:
            return 
         
        for subtree in self.tree["trees"]:
            if self.tree["trees"][subtree]["val"] == self.tree["val"]:
                move = subtree.replace("(","").replace(")","").replace(" ","").split(",")
                logging.info("Making move: %s", subtree)
                self.player_move = self.make_move(
                    board = self.gameboard,
                    possible_lines = self.line_set,
                    first_point = (int(move[0]), int(move[1])),
                    second_point = (int(move[2]), int(move[3])),
                    current_move = self.player_move,
                    score = self.score
                )
                self.draw_line(
                    self.button_canvas,
                    (int(move[0]), int(move[1])),
                    (int(move[2]), int(move[3]))
                )
                self.wait_move()
                return

    def reset(self, size):
        """Function responsible for setting default values"""

        logging.debug("reseting")

        # Setup gameboard itself
        self.start_gameboard(size)

        # Reset computer stuff
        if self.tree is not None:
            self.tree = self.full_tree

        # Setup player stuff
        self.player_move = None
        self.score = [0, 0]

        # Setup lines
        self.line_set = set()
        for y_index in range(self.boardsize[0]):
            for x_index in range(self.boardsize[1]):
                if y_index + 1 != self.boardsize[0]:
                    self.line_set.add(((y_index, x_index),(y_index + 1, x_index)))
                if x_index + 1 != self.boardsize[1]:
                    self.line_set.add(((y_index, x_index),(y_index, x_index + 1)))

        # Define UI
        if self.window_frame:
            self.window_frame.destroy()
        else:
            self.window_frame = None

        self.selected_button = ()
        self.display_menu()

    def display_menu(self):
        """Function to display the slection menu of who goes first"""

        if self.window_frame:
            self.window_frame.destroy()

        self.window_frame = tk.Frame(self.window)

        menu_text = tk.Label(
            self.window_frame,
            text="Chose who goes first:"
        )

        computer_btn = tk.Button(
            self.window_frame,
            text="Computer",
            command=lambda: self.display_game(2)
        )
        human_btn = tk.Button(
            self.window_frame,
            text="Human",
            command=lambda: self.display_game(1)
        )

        menu_text.pack()
        computer_btn.pack()
        human_btn.pack()

        self.window_frame.pack()

    def draw_char(self, slot):
        """Function to draw a char"""
        # (125, 130, 90, 95) 3x3

        scales = (125, 130, 90, 95)
        if self.player_move == 2:
            self.button_canvas.create_text(
                scales[0]+slot[1]*scales[1],
                scales[2]+slot[0]*scales[3],
                text="C"
            )
        else:
            self.button_canvas.create_text(
                scales[0]+slot[1]*scales[1],
                scales[2]+slot[0]*scales[3],
                text="P"
            )

    def draw_line(self, canvas, first_point, second_point):
        """Function to draw a line between two points"""
        # (63, 127, 47, 91) 3x3
        scales = (63, 127, 47, 91)
        canvas.create_line(
            scales[0]+first_point[1]*scales[1], scales[2]+first_point[0]*scales[3],
            scales[0]+second_point[1]*scales[1], scales[2]+second_point[0]*scales[3],
            fill="red",
            width="2"
        )

    def display_game(self, first_move):
        """Function to display the gamescreen"""

        def handle_button_click(event=None):
            if not event:
                return
            button = event.widget
            y_location = button.grid_info()["row"]
            x_location = button.grid_info()["column"]

            if button.cget('bg') == "gray": # If button is the selected button
                button.configure(
                    bg="#d9d9d9"
                )
                self.selected_button = ()
                logging.debug("Selected button unset")
            else:
                if len(self.selected_button) == 0: # If no button is selected
                    button.configure(
                        bg="gray"
                    )
                    self.selected_button = (y_location, x_location)
                    logging.debug("Selected button set")
                else:
                    # Check if the second button is valid
                    if (
                        abs(self.selected_button[0] - y_location) +
                        abs(self.selected_button[1] - x_location)
                    ) == 1:
                        self.player_move = self.make_move(
                            board = self.gameboard,
                            possible_lines = self.line_set,
                            first_point = self.selected_button,
                            second_point = (y_location, x_location),
                            current_move = self.player_move,
                            score = self.score
                        )
                        button_grid.grid_slaves(
                            row=self.selected_button[0],
                            column=self.selected_button[1]
                        )[0].configure(
                            bg="#d9d9d9"
                        )
                        self.draw_line(
                            self.button_canvas,
                            self.selected_button,
                            (y_location, x_location)
                        )
                        self.selected_button = ()
                        self.wait_move()
                    else:
                        logging.info("Invalid line")

        self.player_move = first_move

        if self.window_frame:
            self.window_frame.destroy()

        self.window_frame = tk.Frame(self.window)

        game_label = tk.Label(
            self.window_frame,
            text="The line game:"
        )
        game_label.grid(
            row=0,
            column=0,
            pady=30
        )

        button_grid = tk.Frame(
            self.window_frame,
            width=100,
            height=100
        )
        button_grid.grid(
            row=2,
            column=0,
            pady=20
        )

        # Background to draw the lines
        self.button_canvas = tk.Canvas(
            button_grid,
            background="white"
        )
        self.button_canvas.grid(
            row=0,
            column=0,
            rowspan=self.boardsize[0],
            columnspan=self.boardsize[1]
        )

        for i in range(self.boardsize[1]):
            button_grid.grid_rowconfigure(i, weight=1)
        for i in range(self.boardsize[0]):
            button_grid.grid_columnconfigure(i, weight=1)

        for y_index in range(self.boardsize[0]):
            for x_index in range(self.boardsize[1]):
                btn = tk.Button(
                    button_grid,
                    text="o",
                    name=f"{y_index*self.boardsize[1] + x_index}",
                    command=handle_button_click
                )
                btn.bind("<Button-1>", handle_button_click)
                btn.grid(
                    column=x_index,
                    row=y_index,
                    padx=20,
                    pady=20
                )

        reset_btn = tk.Button(
            self.window_frame,
            text="Reset!",
            command=lambda: self.reset(self.boardsize)
        )
        reset_btn.grid(
            row=1,
            column=0
        )
        self.window_frame.pack()
        self.wait_move()

    def print_to_terminal(self):
        """Function to display the gameboard"""

        logging.info("\n%s", self.gameboard)
        logging.info("Player 1: %s", self.score[0])
        logging.info("Player 2: %s", self.score[1])
        if self.player_move == 2:
            logging.info("Computers move")
        else:
            logging.info("Players move")

    def value_to_bits(self, value):
        """Convert the user inputed number to binary"""
        output_string = format(value, 'b')

        while len(output_string) < 4:
            output_string = "0" + output_string

        return output_string

    def start_gameboard(self, size):
        """Function to handle setting up the gameboard"""

        self.boardsize = size # y x
        self.gameboard = np.zeros(
            shape=self.boardsize,
            dtype=int
        )

    def check_point(self, board, first_point, second_point, tree_generation=False):
        """Function to check if a line between two dots would result in points"""
        points = 0

        first_point_bin_str = self.value_to_bits(
            board[first_point[0]][first_point[1]]
        )
        second_point_bin_str = self.value_to_bits(
            board[second_point[0]][second_point[1]]
        )

        if first_point[0] == second_point[0]: # Check if the points are on the same y
            #   5|6   6|5
            #   1|2   2|1
            #   3|4   4|3
            if (
                first_point_bin_str[3] == "1" and # 1 has line to 3
                second_point_bin_str[3] == "1" # 2 has line to 4
            ):
                if (
                    first_point[1] - 1 == second_point[1] and # 2 1
                    self.value_to_bits(
                        board[first_point[0] + 1][first_point[1]]
                    )[0] == "1" # 3 has line to 4
                ):
                    if not tree_generation:
                        self.draw_char(second_point)
                    points += 1

                elif (
                    first_point[1] + 1 == second_point[1] and # 1 2
                    self.value_to_bits(
                        board[second_point[0] + 1][second_point[1]]
                    )[0] == "1" # 3 has line to 4
                ):
                    if not tree_generation:
                        self.draw_char(first_point)
                    points += 1

            if (
                first_point_bin_str[2] == "1" and # 1 has line to 5
                second_point_bin_str[2] == "1" # 2 has line to 6
            ):
                if (
                    first_point[1] - 1 == second_point[1] and # 2 1
                    self.value_to_bits(
                        board[first_point[0] - 1][first_point[1]]
                    )[0] == "1" # 5 has line to 6
                ):
                    if not tree_generation:
                        self.draw_char((second_point[0] - 1, second_point[1]))
                    points += 1

                elif (
                    first_point[1] + 1 == second_point[1] and # 1 2
                    self.value_to_bits(
                        board[second_point[0] - 1][second_point[1]]
                    )[0] == "1" # 5 has line to 6
                ):
                    if not tree_generation:
                        self.draw_char((first_point[0] - 1, first_point[1]))
                    points += 1

        elif first_point[1] == second_point[1]: # Check if the points are on the same x
            #   5|6   1|2   3|4
            #   6|5   2|1   4|3

            if (
                first_point_bin_str[1] == "1" and # 1 has line to 3
                second_point_bin_str[1] == "1" # 2 has line to 4
            ):
                if (
                    first_point[0] - 1 == second_point[0] and # 2
                    self.value_to_bits(                       # 1
                        board[second_point[0]][second_point[1] + 1]
                    )[3] == "1" # 3 has line to 4
                ):
                    if not tree_generation:
                        self.draw_char(second_point)
                    points += 1

                elif (
                    first_point[0] + 1 == second_point[0] and # 1
                    self.value_to_bits(                       # 2
                        board[first_point[0]][first_point[1] + 1]
                    )[3] == "1" # 3 has line to 4
                ):
                    if not tree_generation:
                        self.draw_char(first_point)
                    points += 1


            if (
                first_point_bin_str[0] == "1" and # 1 has line to 5
                second_point_bin_str[0] == "1" # 2 has line to 6
            ):
                if (
                    first_point[0] - 1 == second_point[0] and # 2
                    self.value_to_bits(                       # 1
                        board[second_point[0]][second_point[1] - 1]
                    )[3] == "1" # 5 has line to 6
                ):
                    if not tree_generation:
                        self.draw_char((second_point[0], second_point[1] - 1))
                    points += 1

                elif (
                    first_point[0] + 1 == second_point[0] and # 1
                    self.value_to_bits(                       # 2
                        board[first_point[0]][first_point[1] - 1]
                    )[3] == "1" # 5 has line to 6
                ):
                    if not tree_generation:
                        self.draw_char((first_point[0], first_point[1] - 1))
                    points += 1

        logging.debug("Gained points: %s", points)
        return points

    def make_move(
        self,
        board,
        possible_lines,
        current_move,
        score,
        first_point,
        second_point,
        tree_generation=False
    ):
        """Function to make a line between two points"""

        def add_line(first_point, second_point):
            # line:
            # 0001 - 1 - Down
            # 0010 - 2 - Up
            # 0100 - 4 - Right
            # 1000 - 8 - Left
            if (first_point, second_point) in possible_lines:
                possible_lines.remove((first_point, second_point))
            if (second_point, first_point) in possible_lines:
                possible_lines.remove((second_point, first_point))

            if first_point[0] == second_point[0]: # Check if the points are on the same y
                if first_point[1] == second_point[1] - 1:
                    #       x
                    #   x   1   2
                    #       x
                    board[first_point[0]][first_point[1]] += 4
                    board[second_point[0]][second_point[1]] += 8

                elif first_point[1] == second_point[1] + 1:
                    #       x
                    #   2   1   x
                    #       x
                    board[first_point[0]][first_point[1]] += 8
                    board[second_point[0]][second_point[1]] += 4

            elif first_point[1] == second_point[1]: # Check if the points are on the same x
                if first_point[0] == second_point[0] - 1:
                    #       x
                    #   x   1   x
                    #       2
                    board[first_point[0]][first_point[1]] += 1
                    board[second_point[0]][second_point[1]] += 2

                elif first_point[0] == second_point[0] + 1:
                    #       2
                    #   x   1   x
                    #       x
                    board[first_point[0]][first_point[1]] += 2
                    board[second_point[0]][second_point[1]] += 1

        if (
            (first_point, second_point) not in possible_lines and
            (second_point, first_point) not in possible_lines
        ):
            logging.debug("Points %s, %s already selected", first_point, second_point)
            return current_move

        add_line(first_point, second_point)
        points = self.check_point(board, first_point, second_point, tree_generation=tree_generation)

        if points == 0:
            current_move = (current_move % 2) + 1
            logging.debug("Flipping move: %s", current_move)
        else:
            score[current_move - 1] += points

        if tree_generation == False:
            if str((first_point, second_point)) in self.tree["trees"]:
                self.tree = self.tree["trees"][str((first_point, second_point))]
            if str((second_point, first_point)) in self.tree["trees"]:
                self.tree = self.tree["trees"][str((second_point, first_point))]
        
        # self.print_to_terminal()

        return current_move

    def generate_gametree(
        self,
        depth = -1,
        filename = ""
    ):
        """The recursive function for generating the gametree"""

        def gametree_rec(
            lines,
            board,
            score = [0, 0],
            move = 1,
            depth = -1, # If set to -1, will generate as far as possible
        ):
            """Function to generate gametree"""

            if depth == 0:
                return "Depth exceeded"

            state = f"l:{lines};s:{score};b:{board};m:{move}"
            
            if state in checked_states:
                return checked_states[state]

            gametree = {
                "score": score,
                "board": board.tolist(),
                "move": move,
                "trees": {}
            }

            for line in lines:

                new_board = np.copy(board)

                new_possible_lines = lines.copy()

                new_current_move = move

                new_score = score.copy()

                new_first_point = line[0]
                new_second_point = line[1]

                new_current_move = self.make_move(
                    new_board,
                    new_possible_lines,
                    new_current_move,
                    new_score,
                    new_first_point,
                    new_second_point,
                    tree_generation=True
                )

                game_subtree = gametree_rec(
                    lines = new_possible_lines,
                    score = new_score,
                    board = new_board,
                    move = new_current_move,
                    depth = depth - 1
                )

                gametree["trees"][str(line)] = game_subtree
                

            if len(lines) == 0:
                gametree["val"] = score[0] - score[1]
                logging.debug("End score diff: %s", gametree["val"])
            else:
                gametree["val"] = None
                for move_key in gametree["trees"]:
                    if (
                        gametree["val"] == None or
                        (gametree["move"] == 1 and gametree["trees"][move_key]["val"] > gametree["val"]) or
                        (gametree["move"] == 2 and gametree["trees"][move_key]["val"] < gametree["val"])
                    ):
                        gametree["val"] = gametree["trees"][move_key]["val"]                       

            checked_states[state] = gametree
            return gametree

        max_moves = 2*self.boardsize[0]*self.boardsize[1]-self.boardsize[0]-self.boardsize[1]
        checked_states = dict()

        if depth == -1:
            logging.info(
                "Generating %s states",
                math.factorial(
                    max_moves
                )
            )
        else:
            variables = 1
            for number in range(
                max_moves,
                max_moves - depth,
                -1
            ):
                variables *= number
            logging.info("Generating %s states", variables)

        start = timeit.default_timer()

        gametree = gametree_rec(
            self.line_set,
            board = np.zeros(shape = self.boardsize, dtype=int),
            depth = depth
        )

        stop = timeit.default_timer()

        logging.info("Tree created in %s seconds", stop - start)
        
        if filename != "":
            logging.info("Writing to '%s'...", filename)
            with open(filename, "w", encoding="utf8") as write_file:
                json.dump(gametree, write_file)
            logging.info("Finished")    

        return gametree


if __name__ == "__main__":

    # Setup logging
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO
    )

    instance = GameBoard((3, 3))

    instance.window.mainloop()
