import frameOptions
import html_generator  
import tpolygon

# Retorna índice da primeira verdade em um lista de Bool
def search_true(x):
    for i in range(len(x)):
        if x[i] == True:
            return i
    raise ValueError("Nothing found on list")

# Retorna o valor do scale para os pontos preencherem width x height
def set_scale(width, height, list_of_points):
    xlim = max([ point.x for point in list_of_points ])
    ylim = max([ point.y for point in list_of_points ])

    xlim *= 1.1
    ylim *= 1.1

    return min(width/xlim, height/ylim)

# Retorna arestas nesse triangulo que não estavam no orgianal
def remaining_edges(triangle):
    edges = []
    for i in range(2):
        if(triangle[i].idx+1 != triangle[i+1].idx):
            edges.append([ triangle[i].idx, triangle[i+1].idx ])
    return edges

class Ear_clipping:
    def __init__(self, initial_polygon, width, height):
        scale = set_scale(width, height, initial_polygon.points)
        self.frame_options = frameOptions.FrameOptions(scale, width, height)

        self.polygon_list = [ initial_polygon ]
        self.frame_list = []

    # Retorna o polígono triangulado e os frames da animação
    def triangulation(self):
        edges = [] # Arestas da triangulação
        triangles = [] # Triangulos da triangulação

        # Adiciona os frames do polígono inicial
        current_polygon = self.polygon_list[0]
        self.frame_list += current_polygon.ear_verification_frames(self.frame_options)

        # Remove orelha e atualiza polígono
        while current_polygon.get_size() > 3:
            new_polygon, new_edge, new_triangle, removal_frames = current_polygon.remove_ear(self.frame_options)

            edges.append(new_edge)
            triangles.append(new_triangle)

            current_polygon = new_polygon
            self.polygon_list.append(current_polygon)

            self.frame_list += removal_frames

        # Adiciona ultimas arestas e triangulos
        edges += remaining_edges(current_polygon.points)
        triangles.append([ point.idx for point in current_polygon.points ])

        # Frame vazio para fim
        # self.frame_list.append(EmptyFrame())

        return tpolygon.TPolygon(self.polygon_list[0], edges, triangles)
    
    def get_polygons(self):
        return self.polygon_list
