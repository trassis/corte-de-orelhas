from queue import Queue
from tframe import TPolygonFrame

class Coloring:
    def __init__(self, tpolygon):
        self.tpolygon = tpolygon
        self.n = tpolygon.number_of_triangles()

        self.points_colors = ["black"] * self.tpolygon.size
        self.frame_list = []

    def solve(self):
        vis = [False]*self.n

        initial_frame = TPolygonFrame(tpolygon=self.tpolygon, points_colors=self.points_colors, description='Polígono Triângulado')
        self.frame_list.append(initial_frame)

        q = Queue()
        q.put(0)
        vis[0] = True

        # Colore os vértices do triangulo inicial
        x,y,z = self.tpolygon.vertices_of_triangle(0) 
        self.points_colors[x] = "blue"
        self.points_colors[y] = "red"
        self.points_colors[z] = "green"

        coloring_frame = TPolygonFrame(tpolygon=self.tpolygon, points_colors=self.points_colors, idx=0, description='Colorindo o triângulo inicial')
        self.frame_list.append(coloring_frame)

        while not q.empty():
            v = q.get()
            for u in self.tpolygon.neighbors(v):
                if not vis[u]:
                    vis[u] = True
                    q.put(u)

                    red_frame = TPolygonFrame(tpolygon=self.tpolygon, points_colors=self.points_colors, idx=u, description='Próximo triângulo a colorir')
                    self.frame_list.append(red_frame)

                    # Obtém nova cor do vértice
                    only_in_v = self.tpolygon.subtract_neighbors(v, u)
                    not_colored = self.tpolygon.subtract_neighbors(u, v)
                    self.points_colors[not_colored] = self.points_colors[only_in_v]

                    colored_frame = TPolygonFrame(tpolygon=self.tpolygon, points_colors=self.points_colors, description='Triângulo colorido!')
                    self.frame_list.append(colored_frame)

        # Conta a quantidade de cada cor
        c1, c2, c3 = 0, 0, 0
        for i in range(len(self.points_colors)):
            if self.points_colors[i] == "blue":
                c1 += 1
            if self.points_colors[i] == "red":
                c2 += 1
            if self.points_colors[i] == "green":
                c3 += 1

        return [ c1, c2, c3 ]
