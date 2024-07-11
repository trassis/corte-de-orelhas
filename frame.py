import os
import frameOptions

def clear_frames():
    pasta = './frames'
    for arquivo in os.listdir(pasta):
        caminho_arquivo = os.path.join(pasta, arquivo)
        try:
            if os.path.isfile(caminho_arquivo):
                os.unlink(caminho_arquivo)

        except Exception as e:
            raise MemoryError(f"Erro ao deletar {caminho_arquivo}: {e}")

def remove_first_and_last_lines(text):
    lines = text.split('\n')
    if len(lines) >= 2:
        ans = '\n'.join(lines[1:len(lines)-2])
        return ans
    else:
        raise ValueError("Should have more than 3 lines")

# Retorna o valor do scale para os pontos preencherem width x height
def set_scale(width, height, list_of_points):
    xlim = max([ point.x for point in list_of_points ])
    ylim = max([ point.y for point in list_of_points ])

    xlim *= 1.1
    ylim *= 1.1

    return min(width/xlim, height/ylim)

# Implementa um frame para um conjunto de pontos
class Frame:
    def __init__(self, points):
        self.points = points
        self.points_colors = ["Black"] * len(points)

        self.frame_options = frameOptions.FrameOptions(scale=1, width=400, height=400)

    # Colore um ponto
    def set_vertex_type(self, idx, new_color):
        if idx >= len(self.points_colors):
            raise IndexError("Índice fora da lista")
        self.points_colors[idx] = new_color

class EFrame(Frame):
    def __init__(self, points, ear_list):
        if points.get_size() != len(ear_list):
            raise ValueError("Polygon and list should be of the same size")

        super().__init__(points)

        # Marca orelhas antigas de azul
        for i in range(len(ear_list)):
            if ear_list[i]:
                self.set_vertex_type(i, "blue")


    def generate_svg(self, background_frame = None):
        # Create the polygon element
        svg_content = f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.frame_options.width}" height="{self.frame_options.height}">\n'

        if background_frame != None:
            big_svg = background_frame.generate_svg()
            svg_content += remove_first_and_last_lines(big_svg)
            svg_content += '\n'

        points_string = ' '.join([f'{point.x*self.frame_options.scale},{point.y*self.frame_options.scale}' for point in self.polygon.points])
        svg_content += f'<polygon points="{points_string}" class="polygon"/>\n'
        
        # Create circles for each vertex with corresponding classes
        for i, point in enumerate(self.polygon.points):
            vertex_class = self.vertex_type[i]
            svg_content += f'<circle cx="{point.x*self.frame_options.scale}" cy="{point.y*self.frame_options.scale}" r="5" class="{vertex_class}_point"/>\n'

        svg_content += '</svg>'

        return svg_content

# Insere uma nova linha antes da última na string original
def insert_before_last(original, new_line):
    lines = original.splitlines()
    lines.insert(-1, new_line)
    return '\n'.join(lines)

class Ear_Frame(Frame):
    def __init__(self, polygon, ear_list, idx):
        super().__init__(polygon, ear_list)

        prev_idx = idx-1 if idx>0 else polygon.get_size()-1
        next_idx = idx+1 if idx<polygon.get_size()-1 else 0
        self.endpoint1 = prev_idx
        self.endpoint2 = next_idx

        # Triângulo sendo verificado fica em vermelho
        self.set_vertex_type(prev_idx, "red")
        self.set_vertex_type(idx, "red")
        self.set_vertex_type(next_idx, "red")

    def generate_svg(self, background_frame):
        svg_content = super().generate_svg(background_frame)

        x1 = self.polygon.points[self.endpoint1].x * self.frame_options.scale
        y1 = self.polygon.points[self.endpoint1].y * self.frame_options.scale
        x2 = self.polygon.points[self.endpoint2].x * self.frame_options.scale
        y2 = self.polygon.points[self.endpoint2].y * self.frame_options.scale

        new_line = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="line_style"/>'
        svg_content = insert_before_last(svg_content, new_line)

        return svg_content

class Triangle_Frame(Frame):
    def __init__(self, triangulated_polygon, color_list): 
        """
        if not isinstance(triangulated_polygon, tpolygon.TPolygon):
            raise TypeError("Erro")
        """

        self.triangle_number = triangulated_polygon.number_of_triangles()
        self.vertex_number =  triangulated_polygon.get_size()
        self.tpolygon = triangulated_polygon

        if self.vertex_number != len(color_list):
            raise ValueError("Vertex_number and colors should have the same size")

        self.triangle_type = ["Blue"]*self.triangle_number
        self.vertex_type = []
        for color in color_list:
            self.vertex_type.append(color)

    def highlight_triangle(self, triangle_idx):
        self.triangle_type[triangle_idx] = "Red"

    def generate_svg(self):
        svg_content = f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.frame_options.width}" height="{self.frame_options.height}">\n'

        points_string = ' '.join([f'{point.x*self.frame_options.scale},{point.y*self.frame_options.scale}' for point in self.tpolygon.get_points()])
        svg_content += f'<polygon points="{points_string}" class="polygon" opacity="{self.frame_options.opacity}"/>\n'
        
        # Desenha vértices
        for i, point in enumerate(self.tpolygon.get_points()):
            vertex_class = self.vertex_type[i]
            svg_content += f'<circle cx="{point.x*self.frame_options.scale}" cy="{point.y*self.frame_options.scale}" r="5" class="vertex_color{vertex_class}" opacity="{self.frame_options.opacity}"/>\n'

        # Desenha triângulos destacados (se houver)
        for i in range(self.triangle_number):
            if self.triangle_type[i] == "Red":
                triangle_string = ' '.join([f'{point.x*self.frame_options.scale},{point.y*self.frame_options.scale}' for point in self.tpolygon.get_points()])
                svg_content += f'<polygon points="{triangle_string}" class="red_triangle" opacity="{self.frame_options.opacity}"/>\n'

        for edge in self.tpolygon.get_edges():
            endpoint1 = edge[0]
            endpoint2 = edge[1]

            x1 = self.tpolygon.get_points()[endpoint1].x * self.frame_options.scale
            y1 = self.tpolygon.get_points()[endpoint1].y * self.frame_options.scale
            x2 = self.tpolygon.get_points()[endpoint2].x * self.frame_options.scale
            y2 = self.tpolygon.get_points()[endpoint2].y * self.frame_options.scale

            svg_content += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="edge_style" opacity="{self.frame_options.opacity}"/>\n'

        svg_content += '</svg>'

        return svg_content
