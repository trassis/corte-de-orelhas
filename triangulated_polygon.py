
class triangulated_polygon:
    def __init__(self, ear_list):
        self.polygon = ear_list[0]
        self.triangles = ear_list[0].size() - 1

    def number_of_triangles(self):
        return self.triangles
