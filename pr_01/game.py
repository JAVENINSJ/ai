#!/usr/bin/python
"""Script to create the box game"""

import logging
import sys

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

        self.start_ui(size)
        self.reset(size)

    def reset(self, size=(4, 4)):
        """Function responsible for setting default values"""

        logging.debug("reseting")

        # Setup gameboard itself
        self.start_gameboard(size)

        # Setup player stuff
        self.player_move = None
        self.score = [0, 0]

        # Setup lines
        self.line_dict = dict()
        for y_index in range(self.boardsize[0]):
            for x_index in range(self.boardsize[1]):
                self.line_dict[(y_index, x_index)] = []

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

    def display_game(self, first_move):
        """Function to display the gamescreen"""

        def draw_line(canvas, first_point, second_point):
            """Function to draw a line between two points"""
            canvas.create_line(
                47+first_point[1]*95, 25+first_point[0]*72,
                47+second_point[1]*95, 25+second_point[0]*72,
                fill="red",
                width="2"
            )

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
                        # logging.info(button)
                        self.make_move(self.selected_button, (y_location, x_location))
                        button_grid.grid_slaves(
                            row=self.selected_button[0],
                            column=self.selected_button[1]
                        )[0].configure(
                            bg="#d9d9d9"
                        )
                        draw_line(
                            button_grid_canvas,
                            self.selected_button,
                            (y_location, x_location)
                        )
                        self.selected_button = ()
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
        button_grid_canvas = tk.Canvas(
            button_grid,
            background="white"
        )
        button_grid_canvas.grid(
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
            command=self.reset
        )
        reset_btn.grid(
            row=1,
            column=0
        )

        self.window_frame.pack()

    def start_ui(self, size):
        """Function to handle starting the UI"""
        self.window = tk.Tk()
        self.window.geometry(f"{size[1]}00x{size[0]+1}00")

    def print_to_terminal(self):
        """Function to display the gameboard"""

        logging.info("\n%s", self.gameboard)
        logging.info("Player 1: %s", self.score[0])
        logging.info("Player 2: %s", self.score[1])
        if self.player_move == 2:
            logging.info("Computers move")
        else:
            logging.info("Play move")

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

    def make_move(self, first_point, second_point):
        """Function to make a line between two points"""

        def add_line(first_point, second_point):
            # line:
            # 0001 - 1 - Down
            # 0010 - 2 - Up
            # 0100 - 4 - Right
            # 1000 - 8 - Left
            self.line_dict[first_point].append(second_point)
            self.line_dict[second_point].append(first_point)

            if first_point[0] == second_point[0]: # Check if the points are on the same y
                if first_point[1] == second_point[1] - 1:
                    #       x
                    #   x   1   2
                    #       x
                    self.gameboard[first_point[0]][first_point[1]] += 4
                    self.gameboard[second_point[0]][second_point[1]] += 8

                elif first_point[1] == second_point[1] + 1:
                    #       x
                    #   2   1   x
                    #       x
                    self.gameboard[first_point[0]][first_point[1]] += 8
                    self.gameboard[second_point[0]][second_point[1]] += 4

            elif first_point[1] == second_point[1]: # Check if the points are on the same x
                if first_point[0] == second_point[0] - 1:
                    #       x
                    #   x   1   x
                    #       2
                    self.gameboard[first_point[0]][first_point[1]] += 1
                    self.gameboard[second_point[0]][second_point[1]] += 2

                elif first_point[0] == second_point[0] + 1:
                    #       2
                    #   x   1   x
                    #       x
                    self.gameboard[first_point[0]][first_point[1]] += 2
                    self.gameboard[second_point[0]][second_point[1]] += 1

        def check_point(first_point, second_point):
            points = 0

            first_point_bin_str = self.value_to_bits(
                self.gameboard[first_point[0]][first_point[1]]
            )
            second_point_bin_str = self.value_to_bits(
                self.gameboard[second_point[0]][second_point[1]]
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
                            self.gameboard[first_point[0] + 1][first_point[1]]
                        )[0] == "1" # 3 has line to 4
                    ):
                        points += 1

                    elif (
                        first_point[1] + 1 == second_point[1] and # 1 2
                        self.value_to_bits(
                            self.gameboard[second_point[0] + 1][second_point[1]]
                        )[0] == "1" # 3 has line to 4
                    ):
                        points += 1

                if (
                    first_point_bin_str[2] == "1" and # 1 has line to 5
                    second_point_bin_str[2] == "1" # 2 has line to 6
                ):
                    if (
                        first_point[1] - 1 == second_point[1] and # 2 1
                        self.value_to_bits(
                            self.gameboard[first_point[0] - 1][first_point[1]]
                        )[0] == "1" # 3 has line to 4
                    ):
                        points += 1

                    elif (
                        first_point[1] + 1 == second_point[1] and # 1 2
                        self.value_to_bits(
                            self.gameboard[second_point[0] - 1][second_point[1]]
                        )[0] == "1" # 3 has line to 4
                    ):
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
                            self.gameboard[second_point[0]][second_point[1] + 1]
                        )[3] == "1" # 3 has line to 4
                    ):
                        points += 1

                    elif (
                        first_point[0] + 1 == second_point[0] and # 1
                        self.value_to_bits(                       # 2
                            self.gameboard[first_point[0]][first_point[1] + 1]
                        )[3] == "1" # 3 has line to 4
                    ):
                        points += 1


                if (
                    first_point_bin_str[0] == "1" and # 1 has line to 5
                    second_point_bin_str[0] == "1" # 2 has line to 6
                ):
                    if (
                        first_point[0] - 1 == second_point[0] and # 2
                        self.value_to_bits(                       # 1
                            self.gameboard[second_point[0]][second_point[1] - 1]
                        )[3] == "1" # 5 has line to 6
                    ):
                        points += 1

                    elif (
                        first_point[0] + 1 == second_point[0] and # 1
                        self.value_to_bits(                       # 2
                            self.gameboard[first_point[0]][first_point[1] - 1]
                        )[3] == "1" # 5 has line to 6
                    ):
                        points += 1

            logging.debug("Gained points: %s", points)
            return points

        if first_point in self.line_dict[second_point]:
            logging.debug("Points already selected")
            return

        add_line(first_point, second_point)
        points = check_point(first_point, second_point)

        if points == 0:
            self.player_move = (self.player_move % 2) + 1
        else:
            self.score[self.player_move - 1] += points

        self.print_to_terminal()

if __name__ == "__main__":

    # Setup logging
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO
    )

    instance = GameBoard((4, 4))
    instance.window.mainloop()
