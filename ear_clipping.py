from polygon import Polygon

class Ear_clipping:
    def __init__(self, initial_polygon):
       self.polygon_list = [initial_polygon]

    def triangulation(self):
        current_polygon = self.polygon_list[0]

        for i in range(current_polygon.get_size()):
            if current_polygon.is_ear(i):
                new_polygon = current_polygon.removed_vertex(i)
                self.polygon_list.append(new_polygon)
                current_polygon = new_polygon
    
    def get_polygons(self):
        return self.polygon_list
    