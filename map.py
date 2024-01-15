import matplotlib.pyplot as plt
from math import floor
from hexagon import Hexagon
import random


# Throw an exception when the number of rows specified by the user is not odd.
class OddRowsException(Exception):
    pass


class Map:
    def __init__(self, rows, bases, seafarers, geographies, numbers, seed=None):
        self.rows = rows
        self.bases = bases
        self.seafarers = seafarers
        self.seed = seed
        self.geographies = geographies
        self.numbers = numbers

    # Determine if inputted rows are odd. This is important as there needs to be a single pivot point
    # in the game of catan (there has to be a single middle row).
    def is_rows_odd(self):
        if self.rows % 2 == 0:
            raise OddRowsException("The number of desired rows is not odd! Please specify an odd number of rows.")
        elif self.rows % 2 == 1:
            return

    def main(self):
        self.is_rows_odd()
        self.draw_board()
        plt.show()

    # Build the coordinates of each hexagon.
    def coordinates(self):
        # Default constants. Best not to touch.
        coords = []
        switch_direction = floor(self.rows / 2)
        hexagons_to_build = self.bases
        hex_x, hex_y = 0, 0.1
        row_start = 0
        x_increment = 0.2
        y_increment = 0.168
        row_start_increment = 0.1

        for row in range(0, self.rows):
            for base in range(0, hexagons_to_build):
                coords.append((hex_x, hex_y))
                hex_x += x_increment
            hex_y += y_increment

            # When the nth row reaches the pivot row then switch direction and build right with less hexagons.
            if row >= switch_direction:
                hexagons_to_build -= 1
                row_start += row_start_increment
            else:
                row_start -= row_start_increment
                hexagons_to_build += 1

            hex_x = row_start

        return coords

    # Build the list of hexagon objects.
    def list_of_hexagons(self):
        fig, ax = plt.subplots()
        plt.axis('off')
        hexagons = []
        list_of_geographies = self.add_n_from_dictionary(self.geographies)
        list_of_numbers = self.add_n_from_dictionary(self.numbers)
        coords = self.coordinates()

        # Get left most and right most x coordinates for seafarers.
        left_most_hex = min(coords, key=lambda t: t[0])[0]
        right_most_hex = max(coords, key=lambda t: t[0])[0]

        number_count = 0
        geography_count = 0

        for count, coordinate in enumerate(coords):
            x, y = coordinate[0], coordinate[1]

            geography = list_of_geographies[geography_count]

            tile = Hexagon(geography, None, x, y, fig, ax)

            # Add left and right most sea tiles as per the seafarers board.
            if self.seafarers:
                if tile.x == left_most_hex or tile.x == right_most_hex:
                    tile.geography = "sea"
                    geography_count -= 1
            # Make sure number count doesn't increase when tile is None.
            if tile.none_tile():
                number_count -= 1

            number = list_of_numbers[number_count]
            # If the geography is a tile without a number then set it to None.
            if tile.none_tile():
                number = None

            tile.number = number

            number_count += 1
            geography_count += 1

            hexagons.append(tile)
        return hexagons

    def draw_board(self):
        coords = self.coordinates()
        hexagons = self.list_of_hexagons()

        left_most_hex = min(coords, key=lambda t: t[0])[0] - 0.1
        right_most_hex = max(coords, key=lambda t: t[0])[0] + 0.1
        bottom_most_hex = min(coords, key=lambda t: t[1])[1] - 0.12
        top_most_hex = max(coords, key=lambda t: t[1])[1] + 0.12

        plt.xlim([left_most_hex, right_most_hex])
        plt.ylim([bottom_most_hex, top_most_hex])
        for hexagon in hexagons:
            hexagon.draw_patch()

    # Add VALUE elements from the KEY to a list.
    # For example: if {'sea': 24}:
    #                   list.append('sea')
    #                   repeat 24 times
    def add_n_from_dictionary(self, dictionary):
        randomised_list = []
        for item in dictionary:
            for i in range(0, dictionary[item]):
                randomised_list.append(item)
        random.seed(self.seed)
        random.shuffle(randomised_list)
        return randomised_list
    