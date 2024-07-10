from queue import Queue
from frame import Triangle_Frame, FrameOptions
import html_generator
import os

def deletar_arquivos_pasta(pasta):
    for arquivo in os.listdir(pasta):
        caminho_arquivo = os.path.join(pasta, arquivo)
        try:
            if os.path.isfile(caminho_arquivo):
                os.unlink(caminho_arquivo)
       
        except Exception as e:
            raise MemoryError(f"Erro ao deletar {caminho_arquivo}: {e}")
class Coloring:
    def __init__(self, triangulated_polygon, height, width, scale):
        self.polygon = triangulated_polygon
        self.n = triangulated_polygon.number_of_triangles()
        self.options = FrameOptions(height, width, scale)

        self.color = [0]*self.polygon.number_of_vertices()
        self.frames = []

    def solve(self):
        vis = [False]*self.n

        initial_frame = Triangle_Frame(self.polygon, self.color, self.options)
        self.frames.append(initial_frame)

        q = Queue()
        q.put(0)
        vis[0] = True

        x,y,z = self.polygon.vertices_of_triangle(0) 
        self.color[x] = 1
        self.color[y] = 2
        self.color[z] = 3

        while not q.empty():
            v = q.get()
            for u in self.polygon.neighbors(v):
                if not vis[u]:
                    vis[u] = True
                    q.put(u)

                    red_frame = Triangle_Frame(self.polygon, self.color, self.options)
                    red_frame.highlight_triangle(u)
                    self.frames.append(red_frame)

                    only_in_v = self.polygon.subtract_neighbors(v, u)
                    not_colored = self.polygon.subtract_neighbors(u, v)
                    self.color[not_colored] = self.color[only_in_v]

                    colored_frame = Triangle_Frame(self.polygon, self.color, self.options)
                    self.frames.append(colored_frame)

    def generate_html(self):
        deletar_arquivos_pasta('./frames')

        for i, frame in enumerate(self.frames):
            with open(f"./frames/frame{i}.svg", "w") as file:
                file.write(frame.generate_svg())

        return html_generator.get(len(self.frames), self.options.width, self.options.height)
