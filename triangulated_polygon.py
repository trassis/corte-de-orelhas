
class Triangulated_Polygon:
    def __init__(self, polygon, new_edges, triangles):
        self.polygon = polygon
        self.new_edges = new_edges
        self.triangles = triangles

    def number_of_triangles(self):
        return self.polygon.get_size() - 2
    
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
    
    def get_edges(self):
        return self.new_edges
    
    def is_adj(t1, t2):
        pontos_comuns = set(t1) & set(t2)
        return len(pontos_comuns) == 2

    def neighbors(self, idx):
        neib = []

        for i in range(len(self.triangles)):
            if i == idx: 
                continue
            if self.is_adj(self.triangles[i], self.triangles[idx]):
                neib.append(i)
                
        return neib
            