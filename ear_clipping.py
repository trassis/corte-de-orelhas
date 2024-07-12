import tpolygon
import epolygon
from frame import Frame, EmptyFrame

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
        self.polygon_list = [ epolygon.EPolygon(copy_polygon=polygon) ]
        self.frame_list = [ Frame(polygon) ]

    # Retorna o polígono triangulado e os frames da animação
    def triangulation(self):
        edges = [] # Arestas da triangulação
        triangles = [] # Triangulos da triangulação

        # Adiciona os frames do polígono inicial
        current_polygon = self.polygon_list[0]
        self.frame_list += current_polygon.ear_verification_frames()

        # Remove orelha e atualiza polígono
        while current_polygon.get_size() > 3:
            new_polygon, new_edge, new_triangle, removal_frames = current_polygon.remove_ear()

            edges.append(new_edge)
            triangles.append(new_triangle)

            current_polygon = new_polygon
            self.polygon_list.append(current_polygon)

            self.frame_list += removal_frames

        # Adiciona ultimo triangulo
        # triangles.append([ point.idx for point in current_polygon.points ])

        # Frame vazio para visualizar o fim
        self.frame_list.append(EmptyFrame())

        # Coloca resultado no plano de fundo
        triangulated = tpolygon.TPolygon(self.polygon_list[0].points, edges, triangles)
        for frame in self.frame_list:
           frame.set_background(triangulated)

        return triangulated

    
    def get_polygons(self):
        return self.polygon_list
