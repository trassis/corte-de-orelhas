from triangulated_polygon import Triangulated_Polygon
import frameOptions
import html_generator  

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

class Ear_clipping:
    def __init__(self, initial_polygon, width, height):
        scale = set_scale(width, height, initial_polygon.points)
        self.frame_options = frameOptions.FrameOptions(scale, width, height)

        self.polygon_list = [ initial_polygon ]
        self.frame_list = []

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

        self.edges = edges
        self.triangles = triangles

        # Frame vazio para fim
        # self.frame_list.append(EmptyFrame())
    
    def get_polygons(self):
        return self.polygon_list
    
    def get_new_edges(self):
        return self.edges

    def get_result(self):
        return Triangulated_Polygon(self.polygon_list[0], self.edges, self.triangles)

    def generate_html(self):
        # Sem background por enquanto
        """
        frame.clear_frames()

        zero_list = [ 0 ]* self.polygon_list[0].get_size()
        background_frame = frame.Triangle_Frame(self.get_result(), zero_list, self.frame_options, 0.2)

        for i, frame in enumerate(self.frame_list):
            with open(f"./frames/frame{i}.svg", "w") as file:
                file.write(frame.generate_svg(background_frame))
        """

        return html_generator.get(len(self.frame_list), self.frame_options.width, self.frame_options.height)
