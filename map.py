import matplotlib.pyplot as plt
from math import floor, sqrt
from hexagon import Hexagon
import random
import numpy as np


# Throw an exception when the number of rows specified by the user is not odd.
class OddRowsException(Exception):
    pass


def dist(coord_1, coord_2):
    x_1, y_1 = coord_1[0], coord_1[1]
    x_2, y_2 = coord_2[0], coord_2[1]

    return sqrt((x_1 - x_2)**2 + (y_1 - y_2)**2)


# Get the 6 closest tiles ID (adjacent tiles) per tile 
def top_6_closest(tiles):
    top_6_closest_tiles_per_subj = []
    k = 6

    for tile_subj_id, tile_subj in enumerate(tiles):
        dist_list = []
        for tile_comp_id, tile_comp in enumerate(tiles):
            if tile_subj_id == tile_comp_id:
                dist_list.append(float('inf'))
                continue
            tile_subj_coord = (tile_subj.x, tile_subj.y)
            tile_comp_coord = (tile_comp.x, tile_comp.y)
            distance = dist(tile_subj_coord, tile_comp_coord)
            dist_list.append(distance)
        top_6 = np.argpartition(np.array(dist_list), k)[0:k]
        top_6_closest_tiles_per_subj.append(top_6.tolist())

    return top_6_closest_tiles_per_subj


class Map:
    def __init__(self, rows, bases, seafarers, geographies, numbers, seed=None):
        # Increment rows by 2 and bases by 1 to increase size of the board for the invisible border tiles.
        self.rows = rows + 2
        self.bases = bases + 1
        self.seafarers = seafarers
        self.seed = seed
        self.geographies = geographies
        self.numbers = numbers
        self.number_catalogue = self.add_n_from_dictionary(self.numbers)
        self.geography_catalogue = self.add_n_from_dictionary(self.geographies)

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
        return

    # Build coordinates of each hexagon by rows. This is to find the second most/least
    # x-value for the blank sea tile in the Seafarers expansion.
    def coord_by_row(self):
        # Default constants. Best not to touch.
        layer_list = []

        switch_direction = floor(self.rows / 2)
        hexagons_to_build = self.bases
        hex_x, hex_y = 0, 0.1
        row_start = 0
        x_increment = 0.2
        y_increment = 0.168
        row_start_increment = 0.1

        for row in range(0, self.rows):
            x_coord = []
            y_coord = []
            for base in range(0, hexagons_to_build):
                x_coord.append(hex_x)
                y_coord.append(hex_y)

                hex_x += x_increment

            hex_y += y_increment
            layer_list.append(list(zip(x_coord, y_coord)))

            # When the nth row reaches the pivot row then switch direction and build right with fewer hexagons.
            if row >= switch_direction:
                hexagons_to_build -= 1
                row_start += row_start_increment
            else:
                row_start -= row_start_increment
                hexagons_to_build += 1

            hex_x = row_start

        return layer_list

    # Use the output of coord_by_row() to get a whole single list of all (x, y) coords.
    def coordinates(self):
        # Un-lists the nested list made from coord_by_row().
        coords = [x for xs in self.coord_by_row() for x in xs]

        return coords

    # Build the list of hexagon objects per row.
    def geography_tiles(self):
        fig, ax = plt.subplots()
        plt.axis('off')
        hexagons = []
        coord_by_row = self.coord_by_row()

        iteration = 0
        for row_number, row in enumerate(coord_by_row):
            for coordinate in row:
                x, y = coordinate[0], coordinate[1]

                tile = Hexagon(None, None, x, y, fig, ax)

                left_most_hex = sorted(row, key=lambda t: t[0])[0][0]
                right_most_hex = sorted(row, reverse=True, key=lambda t: t[0])[0][0]

                # Check if the tile belongs to the border tiles.
                if (row_number == 0 or
                        row_number == (self.rows - 1) or
                        tile.x == left_most_hex or
                        tile.x == right_most_hex):
                    tile.geography = "border"
                    hexagons.append(tile)
                    continue

                # Add left and right most sea tiles as per the seafarers board.
                # Decrease geography_count by 1 to essentially skip this iteration of the for loop.
                if self.seafarers:
                    second_left_most_hex = sorted(row, key=lambda t: t[0])[1][0]
                    second_right_most_hex = sorted(row, reverse=True, key=lambda t: t[0])[1][0]
                    if (row_number == floor(self.rows/2) and
                            (tile.x == second_left_most_hex or tile.x == second_right_most_hex)):
                        tile.geography = "sea"
                        hexagons.append(tile)
                        continue

                tile.geography = self.geography_catalogue[iteration]

                iteration += 1

                hexagons.append(tile)

        return hexagons

    # Generate number tiles (dependent on geography_tiles())
    def number_tiles(self):
        tiles = self.geography_tiles()
        number_count = 0
        for tile in tiles:
            if tile.none_tile():
                continue
            tile.number = self.number_catalogue[number_count]
            number_count += 1

        return tiles

    # Checks if the tile is eligible to be a red number.
    # A tile can be a red number (6 or 8 by default) if it is not surrounded by at least 1 other red number tile.
    def is_red_number_eligible(self):
        adjacency_mat = top_6_closest(self.number_tiles())
        return adjacency_mat

    # Return the nearest 6 tiles.
    def get_nearest_tiles(self):
        return

    def draw_board(self):
        coords = self.coordinates()
        hexagons = self.number_tiles()

        # Get left and right most hexes to get x and y limits for the plot.
        left_most_hex = min(coords, key=lambda t: t[0])[0] - 0.1
        right_most_hex = max(coords, key=lambda t: t[0])[0] + 0.1
        bottom_most_hex = min(coords, key=lambda t: t[1])[1] - 0.12
        top_most_hex = max(coords, key=lambda t: t[1])[1] + 0.12

        plt.xlim([left_most_hex, right_most_hex])
        plt.ylim([bottom_most_hex, top_most_hex])
        [hexagon.draw_patch() for hexagon in hexagons]

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
        
