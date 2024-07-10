from queue import Queue

class Coloring:
    def __init__(self, triangulated_polygon):
        self.polygon = triangulated_polygon
        self.n = triangulated_polygon.number_of_triangles()

        self.color = [-1]*self.polygon.number_of_vertices()
        self.frames = []

    def solve(self):
        vis = [False]*self.n

        q = Queue()
        q.put(0)
        vis[0] = True

        x,y,z = self.polygon.vertices_of_triangle(0) 
        self.color[x] = 0
        self.color[y] = 1
        self.color[z] = 1

        while not q.empty():
            v = q.get()
            for u in self.polygon.neighbors(v):
                if not vis[u]:
                    vis[u] = True
                    q.put(u)

                    only_in_v = self.polygon.subtract_neighbors(v, u)
                    not_colored = self.polygon.subtract_neighbors(u, v)
                    self.color[not_colored] = self.color[only_in_v]
