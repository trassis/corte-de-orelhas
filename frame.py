from polygon import Polygon
import os

def clear_frames():
    pasta = './frames'
    for arquivo in os.listdir(pasta):
        caminho_arquivo = os.path.join(pasta, arquivo)
        try:
            if os.path.isfile(caminho_arquivo):
                os.unlink(caminho_arquivo)

        except Exception as e:
            raise MemoryError(f"Erro ao deletar {caminho_arquivo}: {e}")

class FrameOptions:
    def __init__(self, scale, widht, height, opacity=1.0):
        self.scale = scale
        self.width = widht
        self.height = height
        self.opacity = opacity

class Frame:
    def __init__(self, polygon, ear_list, options):
        if not isinstance(polygon, Polygon):
            raise TypeError("Object polygon should be of class Polygon")
        if not isinstance(options, FrameOptions):
            raise TypeError("Object options should be of class FrameOptions")
        if polygon.get_size() != len(ear_list):
            raise ValueError("Polygon and list should be of the same size")

        self.frame_options = options
        self.polygon = polygon
        self.vertex_type = ["black"]*polygon.get_size()
        # Marca orelhas antigas de azul
        for i in range(len(ear_list)):
            if ear_list[i]:
                self.set_vertex_type(i, "blue")

    def set_vertex_type(self, idx, new_type):
        if idx >= len(self.vertex_type):
            raise IndexError("Índice fora da lista")
        self.vertex_type[idx] = new_type

    def generate_svg(self):
        # Create the polygon element
        svg_content = f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.frame_options.width}" height="{self.frame_options.height}">\n'

        points_string = ' '.join([f'{point.x*self.frame_options.scale},{point.y*self.frame_options.scale}' for point in self.polygon.points])
        svg_content += f'<polygon points="{points_string}" class="polygon"/>\n'
        
        # Create circles for each vertex with corresponding classes
        for i, point in enumerate(self.polygon.points):
            vertex_class = self.vertex_type[i]
            svg_content += f'<circle cx="{point.x*self.frame_options.scale}" cy="{point.y*self.frame_options.scale}" r="5" class="{vertex_class}_point"/>\n'

        svg_content += '<svg/>'

        return svg_content

# Insere uma nova linha antes da última na string original
def insert_before_last(original, new_line):
    lines = original.splitlines()
    lines.insert(-1, new_line)
    return '\n'.join(lines)

class Ear_Frame(Frame):
    def __init__(self, polygon, ear_list, options, idx):
        super().__init__(polygon, ear_list, options)

        prev_idx = idx-1 if idx>0 else polygon.get_size()-1
        next_idx = idx+1 if idx<polygon.get_size()-1 else 0
        self.endpoint1 = prev_idx
        self.endpoint2 = next_idx

        # Triângulo sendo verificado fica em vermelho
        self.set_vertex_type(prev_idx, "red")
        self.set_vertex_type(idx, "red")
        self.set_vertex_type(next_idx, "red")


    def generate_svg(self):
        svg_content = super().generate_svg()

        x1 = self.polygon.points[self.endpoint1].x * self.frame_options.scale
        y1 = self.polygon.points[self.endpoint1].y * self.frame_options.scale
        x2 = self.polygon.points[self.endpoint2].x * self.frame_options.scale
        y2 = self.polygon.points[self.endpoint2].y * self.frame_options.scale

        new_line = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="line_style"/>'
        svg_content = insert_before_last(svg_content, new_line)

        return svg_content

class Triangle_Frame:
    def __init__(self, triangulated_polygon, color_list, options): 
        self.triangle_number = triangulated_polygon.number_of_triangles()
        self.vertex_number =  triangulated_polygon.number_of_vertices()
        self.tpolygon = triangulated_polygon

        if self.vertex_number != len(color_list):
            raise ValueError("Vertex_number and colors should have the same size")

        self.triangle_type = ["Blue"]*self.triangle_number
        self.vertex_type = []
        for color in color_list:
            self.vertex_type.append(color)

        self.frame_options = options

    def highlight_triangle(self, triangle_idx):
        self.triangle_type[triangle_idx] = "Red"

    def generate_svg(self):
        svg_content = f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.frame_options.width}" height="{self.frame_options.height}" opacity="{self.frame_options.opacity}">\n'

        points_string = ' '.join([f'{point.x*self.frame_options.scale},{point.y*self.frame_options.scale}' for point in self.tpolygon.get_points()])
        svg_content += f'<polygon points="{points_string}" class="polygon"/>\n'
        
        # Desenha vértices
        for i, point in enumerate(self.tpolygon.get_points()):
            vertex_class = self.vertex_type[i]
            svg_content += f'<circle cx="{point.x*self.frame_options.scale}" cy="{point.y*self.frame_options.scale}" r="5" class="vertex_color{vertex_class}"/>\n'

        # Desenha triângulos destacados (se houver)
        for i in range(self.triangle_number):
            triangle_string = ' '.join([f'{point.x*self.frame_options.scale},{point.y*self.frame_options.scale}' for point in self.tpolygon.get_points()])
            svg_content += f'<polygon points="{triangle_string}" class="red_triangle"/>\n'

        # Desenha arestas
        for edge in self.tpolygon.get_edges():
            endpoint1 = edge[0]
            endpoint2 = edge[1]

            x1 = self.tpolygon.get_points()[endpoint1].x * self.frame_options.scale
            y1 = self.tpolygon.get_points()[endpoint1].y * self.frame_options.scale
            x2 = self.tpolygon.get_points()[endpoint2].x * self.frame_options.scale
            y2 = self.tpolygon.get_points()[endpoint2].y * self.frame_options.scale

            svg_content = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="edge_style"/>'

        svg_content += '<svg/>'

        return svg_content



