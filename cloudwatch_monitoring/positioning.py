"""
module for keeping track of widget position on the dashboard

"""


class Positioning:
    # set starting and default values for widget self and dimensions
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 24
        self.height = 3
        self.max_width = 24
    
    def iterate_positioning(self):
        self.x += self.width
        if self.x + self.width > self.max_width:
            self.x = 0
            self.y += self.height
