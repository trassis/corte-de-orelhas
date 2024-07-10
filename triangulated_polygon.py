
class triangulated_polygon:
    def __init__(self, polygon, new_edges, triangle_edges):
        

    def number_of_triangles(self):
        return self.triangles
    
    def number_of_vertices(self):
        return self.polygon.get_size()

    def vertices_of_triangle(self, idx):
        return self.triangles[idx]

    # quem ta em v mas não esta u
    def subtract_neighbors(self, v, u):
        ret = []
        for i in self.vertices_of_triangle(v):
            ok = True
            for j in self.vertices_of_triangle(u):
                if i == j:
                    ok = False
            if ok:
                ret.append(i)

        if len(ret) != 1:
            raise ValueError("This should be only one!")

        return ret[0]

    def get_points(self):
        return self.polygon.get_points()