from polygon import Polygon

# Retorna índice da primeira verdade em um lista de Bool
def search_true(x):
    for i in range(len(x)):
        if x[i] == True:
            return i
    raise ValueError("Nothing found on list")

class Ear_clipping:
    def __init__(self, initial_polygon):
        self.polygon_list = [initial_polygon]

    def triangulation(self):
        current_polygon = self.polygon_list[0]
        ear_list = [ current_polygon.is_ear(i) for i in range(current_polygon.get_size()) ]

        print(current_polygon.get_size())
        print(ear_list)

        while current_polygon.get_size() > 3:
            to_be_removed = search_true(ear_list)
            ear_list.pop(to_be_removed)
            new_polygon = current_polygon.removed_vertex(to_be_removed)

            previous_index = to_be_removed-1 if to_be_removed > 0 else new_polygon.get_size()-1
            next_index = to_be_removed if to_be_removed < new_polygon.get_size()-1 else 0

            ear_list[previous_index] = new_polygon.is_ear(previous_index)
            ear_list[next_index] = new_polygon.is_ear(next_index)

            current_polygon = new_polygon
            self.polygon_list.append(current_polygon)
    
    def get_polygons(self):
        return self.polygon_list

    def generate_html(self):
        pass
    
