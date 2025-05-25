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

def add_n_from_dictionary(seed, dictionary):
        randomised_list = []
        for item in dictionary:
            for i in range(0, dictionary[item]):
                randomised_list.append(item)
        random.seed(seed)
        random.shuffle(randomised_list)
        return randomised_list


class Map:
    def __init__(self, rows, bases, seafarers, geographies, numbers, seed=None):
        # Increment rows by 2 and bases by 1 to increase size of the board for the invisible border tiles.
        self.rows = rows + 2
        self.bases = bases + 1
        self.seafarers = seafarers
        self.seed = seed
        self.numbers = add_n_from_dictionary(seed, numbers)
        self.geographies = add_n_from_dictionary(seed, geographies)
        self.fig, self.ax = plt.subplots()

    def is_rows_odd(self):
        """
        Determine if inputted rows are odd. This is important as there needs to be a single pivot point
        in the game of catan (there has to be a single middle row).
        """
        if self.rows % 2 == 0:
            raise OddRowsException("The number of desired rows is not odd! Please specify an odd number of rows.")
        elif self.rows % 2 == 1:
            return

    def main(self):
        self.is_rows_odd()
        
        coords = self.coord_by_row()
        tiles = self.geography_tiles(coord_by_row=coords)
        coordinates = [x for xs in coords for x in xs]
        hexagons = self.number_tiles(tiles)
        self.draw_board(coordinates, hexagons)
        
        # self.is_red_number_eligible(hexagons)
        
        plt.show()
        return

    def coord_by_row(self):
        """
        Build coordinates of each hexagon by rows. This is to find the second most/least
        x-value for the blank sea tile in the Seafarers expansion.
        """
        
        X_INCREMENT = 0.2
        Y_INCREMENT = 0.168
        ROW_START_INCREMENT = 0.1
        SWITCH_DIRECTION = floor(self.rows / 2)
        
        hexagons_to_build = self.bases
        hex_x, hex_y = 0, 0.1
        row_start = 0
        layer_list = []
        
        for row in range(0, self.rows):
            x_coord = []
            y_coord = []
            for base in range(0, hexagons_to_build):
                x_coord.append(hex_x)
                y_coord.append(hex_y)

                hex_x += X_INCREMENT

            hex_y += Y_INCREMENT
            layer_list.append(list(zip(x_coord, y_coord)))

            # When the nth row reaches the pivot row then switch direction and build right with fewer hexagons.
            if row >= SWITCH_DIRECTION:
                hexagons_to_build -= 1
                row_start += ROW_START_INCREMENT
            else:
                row_start -= ROW_START_INCREMENT
                hexagons_to_build += 1

            hex_x = row_start

        return layer_list

    def geography_tiles(self, coord_by_row):
        """
        Build the list of hexagon objects per row.
        """
        
        plt.axis('off')
        hexagons = []

        iteration = 0
        for row_number, row in enumerate(coord_by_row):
            for coordinate in row:
                x, y = coordinate[0], coordinate[1]

                tile = Hexagon(None, None, x, y, self.fig, self.ax)

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

                tile.geography = self.geographies[iteration]

                iteration += 1

                hexagons.append(tile)

        return hexagons

    def number_tiles(self, tiles):
        """
        Generate number tiles
        """
        number_count = 0
        for tile in tiles:
            if tile.none_tile():
                continue
            tile.number = self.numbers[number_count]
            number_count += 1

        return tiles

    def is_red_number_eligible(self, hexagons):
        """
        Checks if the tile is eligible to be a red number.
        A tile can be a red number (6 or 8 by default) if it is not surrounded by at least 1 other red number tile.
        (NOT IMPLEMENTED)
        """
        adjacency_mat = top_6_closest(hexagons)
        return adjacency_mat

    def get_nearest_tiles(self):
        """
        Return the nearest 6 tiles.
        """
        return

    def draw_board(self, coords, hexagons):

        # Get left and right most hexes to get x and y limits for the plot.
        LEFT_MOST_HEX = min(coords, key=lambda t: t[0])[0] - 0.1
        RIGHT_MOST_HEX = max(coords, key=lambda t: t[0])[0] + 0.1
        BOTTOM_MOST_HEX = min(coords, key=lambda t: t[1])[1] - 0.12
        TOP_MOST_HEX = max(coords, key=lambda t: t[1])[1] + 0.12

        plt.xlim([LEFT_MOST_HEX, RIGHT_MOST_HEX])
        plt.ylim([BOTTOM_MOST_HEX, TOP_MOST_HEX])
        [hexagon.draw_patch() for hexagon in hexagons]

    # Add VALUE elements from the KEY to a list.
    # For example: if {'sea': 24}:
    #                   list.append('sea')
    #                   repeat 24 times
    def add_n_from_dictionary(self, dictionary):
        """
        Add VALUE elements from the KEY to a list.
        For example: if {'sea': 24}:
                           list.append('sea')
                           repeat 24 times
        """
        randomised_list = []
        for item in dictionary:
            for i in range(0, dictionary[item]):
                randomised_list.append(item)
        random.seed(self.seed)
        random.shuffle(randomised_list)
        return randomised_list
        

if __name__ == '__main__':
    seafarers_geography = {
        "sea": 17,
        "desert": 0,
        "gold_fields": 2,
        "fields": 5,
        "hills": 4,
        "mountains": 4,
        "pastures": 5,
        "forests": 5}
    seafarers_numbers = {
        2: 2,
        3: 3,
        4: 3,
        5: 3,
        6: 2,
        8: 2,
        9: 3,
        10: 3,
        11: 2,
        12: 2}
    Map(7, 5, True, seafarers_geography, seafarers_numbers).main()
