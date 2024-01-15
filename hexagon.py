import matplotlib.patches as mpatches


class Hexagon:
    def __init__(self, geography, number, x, y, fig, ax, vertices=6, radius=0.1):
        self.geography = geography
        self.number = number
        self.x = x
        self.y = y
        self.vertices = vertices
        self.radius = radius
        self.ax = ax
        self.fig = fig

    def is_red_number(self):
        red_numbers = [6, 8]
        if self.number in red_numbers:
            return True
        else:
            return False

    def draw_patch(self):
        self.draw_number()
        self.ax.add_patch(self.create_border())
        self.ax.add_patch(self.create_hexagon())

    def create_hexagon(self):
        return mpatches.RegularPolygon((self.x, self.y),
                                       self.vertices,
                                       radius=self.radius,
                                       color=self.set_color())

    def create_border(self):
        return mpatches.RegularPolygon((self.x, self.y),
                                       self.vertices,
                                       radius=self.radius * 1.06,
                                       color="black")

    def draw_number(self):
        if self.is_red_number():
            col = "red"
        else:
            col = "black"
        self.ax.text(self.x, self.y - 0.025, self.number, ha="center", family='sans-serif', size=20, color=col)

    def set_color(self):
        geo_to_color = {
            "sea": "skyblue",
            "hills": "sienna",
            "pastures": "lawngreen",
            "mountains": "darkgrey",
            "fields": "gold",
            "forests": "darkgreen",
            "gold_fields": "khaki",
            "desert": "moccasin"
        }

        return geo_to_color[self.geography]

    def none_tile(self):
        none_tiles = ["sea", "desert"]
        if self.geography in none_tiles:
            return True
        else:
            return False
