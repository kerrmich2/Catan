import matplotlib.patches as mpatches


class Hexagon:
    def __init__(self, geography, number, x, y, fig, ax, radius, vertices=6, is_red_number_eligible=None):
        self._geography = geography
        self._number = number
        self._x = x
        self._y = y
        self.vertices = vertices
        self.radius = radius
        self.ax = ax
        self.fig = fig
        self.is_red_number_eligible = is_red_number_eligible
        self._update_name()

    def _update_name(self):
        self.name = f'{self._geography}_{self._number}_({self._x},{self._y})'

    @property
    def geography(self):
        return self._geography

    @geography.setter
    def geography(self, value):
        self._geography = value
        self._update_name()

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        self._number = value
        self._update_name()

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self._update_name()

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self._update_name()

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

        if self.geography == "border":
            border_color = "white"
        else:
            border_color = "black"
        return mpatches.RegularPolygon((self.x, self.y),
                                       self.vertices,
                                       radius=self.radius,
                                       color=border_color)


    def draw_number(self):
        if self.is_red_number():
            col = "red"
        else:
            col = "black"
        self.ax.text(self.x, self.y, self.number, ha="center", family='sans-serif', size=20*self.radius*10, color=col)

    def set_color(self):
        geo_to_color = {
            "sea": "skyblue",
            "hills": "sienna",
            "pastures": "lawngreen",
            "mountains": "darkgrey",
            "fields": "gold",
            "forests": "darkgreen",
            "gold_fields": "khaki",
            "desert": "moccasin",
            "border": "white"
        }

        return geo_to_color[self.geography]

    def none_tile(self):
        none_tiles = ["sea", "desert", "border"]
        if self.geography in none_tiles:
            return True
        else:
            return False
