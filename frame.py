from polygon import Polygon

class Frame:
    def __init__(self, polygon):
        self.polygon = polygon

    def generate_svg(self):
        raise NotImplementedError("Subclass must implement abstract method")

class Ear_Frame(Frame):
    def generate_svg(self):
        pass

class Neighbor_Frame(Frame):
    def generate_svg(self):
        pass