from polygon import Polygon

class Ear_clipping:
    def __init__(self, initial_polygon):
       self.polygon_list = [initial_polygon]

    def triangulation(self):
        current_polygon = self.polygon_list[0]

        for i in range(current_polygon.get_size()):
            print("yes")
            if current_polygon.is_ear(i):
                print("yes")
                new_points = current_polygon.remove_vertex(i)
                current_polygon = Polygon(new_points)
                self.polygon_list.append(current_polygon)
    
    def get_polygons(self):
        return self.polygon_list
            