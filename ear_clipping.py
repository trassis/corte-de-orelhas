import tpolygon
from epolygon import EPolygon
from eframe import EarFrame, EmptyEarFrame

# Retorna índice da primeira verdade em um lista de Bool
def search_true(x):
    for i in range(len(x)):
        if x[i] == True:
            return i
    raise ValueError("Nothing found on list")

# Retorna arestas nesse triangulo que não estavam no orgianal
def remaining_edges(triangle):
    edges = []
    for i in range(2):
        if(triangle[i].idx+1 != triangle[i+1].idx):
            edges.append([ triangle[i].idx, triangle[i+1].idx ])
    return edges

class Ear_clipping:
    def __init__(self, polygon):
        initial_epolygon = EPolygon(copy_polygon=polygon) 

        self.polygon_list = [ initial_epolygon ]
        self.frame_list = [ EarFrame(initial_epolygon, description='Polígono inicial') ]

    # Retorna o polígono triangulado e os frames da animação
    def triangulation(self):
        edges = [] # Arestas da triangulação
        triangles = [] # Triangulos da triangulação

        # Computa todas as orelhas iniciais
        current_polygon = self.polygon_list[0]
        for i in range(current_polygon.size):
            update_frames = current_polygon.update_ear_list(i)
            self.frame_list += update_frames

        # Remove orelhas até poligono ter 3 pontos
        while current_polygon.get_size() > 3:
            new_polygon, new_edge, new_triangle, removal_frames = current_polygon.remove_ear()

            edges.append(new_edge)
            triangles.append(new_triangle)

            current_polygon = new_polygon
            self.polygon_list.append(current_polygon)

            self.frame_list += removal_frames

        # Adiciona ultimo triangulo
        triangles.append([ point.idx for point in current_polygon.points ])

        # Frame vazio para visualizar o fim
        self.frame_list.append(EmptyEarFrame('Polígono triangulado!'))

        # Coloca resultado no plano de fundo
        triangulated = tpolygon.TPolygon(self.polygon_list[0].points, edges, triangles)
        for frame in self.frame_list:
           frame.set_background(triangulated)

        return triangulated

    def get_polygons(self):
        return self.polygon_list
