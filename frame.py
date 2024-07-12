from frameOptions import FrameOptions

# Implementa um frame para um conjunto de pontos
class Frame:
    def __init__(self, polygon, points_colors=[], opacity=1.0):
        if polygon == None:
            self.points = []
            self.points_colors = []
        else:
            self.points = polygon.points

            if len(points_colors) == 0:
                self.points_colors = ["black"] * len(polygon.points)
            else:
                self.points_colors = points_colors

        self.height = FrameOptions.height
        self.width = FrameOptions.width
        self.scale = FrameOptions.scale
        self.opacity = opacity

        self.background_svg = ''
        self.middle_ground_svg = self._get_middle_ground()
        self.foreground_svg = ''

    def _get_middle_ground(self):
        # Cor de fundo do poligono
        points_string = ' '.join([f'{round(point.x*self.scale, 3)},{round(point.y*self.scale, 3)}' for point in self.points])
        svg_content = f'<polygon points="{points_string}" class="polygon" opacity="{self.opacity}"/>\n'
        # Desenha os pontos
        for i, point in enumerate(self.points):
            color = self.points_colors[i]
            svg_content += f'<circle cx="{round(point.x*self.scale, 3)}" cy="{round(point.y*self.scale, 3)}" class="{color}_point" opacity="{self.opacity}"/>\n'

        return svg_content

    # Todo frame possui cor de fundo para poligono e cor para os pontos
    # Pode adicionar um plano de fundo (ex: polígono triangulado)
    # Pode adicionar um plano de frente (ex: arestas de uma triangulação)
    def generate_svg(self):
        svg_content = f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}">\n'

        # Adiciona os planos
        svg_content += self.background_svg
        svg_content += self.middle_ground_svg
        svg_content += self.foreground_svg

        svg_content += '</svg>'

        return svg_content
        
# Frame que representa um tpolygon
class TPolygonFrame(Frame):
    def __init__(self, tpolygon, opacity=1.0, color_list=None, idx=-1): 
        super().__init__(polygon=tpolygon, opacity=opacity)

        self.triangle_number = tpolygon.number_of_triangles()
        self.vertex_number = tpolygon.get_size()
        self.tpolygon = tpolygon

        if color_list == None:
            color_list = ["black"] * self.vertex_number

        self.triangles_colors = ["blue"]*self.triangle_number

        if idx != -1:
            self.triangles_colors[idx] = "red"

        self.foreground_svg += self._get_edges_svg()
        self.foreground_svg = self._get_foreground()

    def _get_foreground(self):
        svg_content = ''
        # Desenha triângulos destacados (se houver)
        for i in range(self.triangle_number):
            if self.triangles_colors[i] == "red":
                triangle_index = self.tpolygon.vertices_of_triangle(i)
                triangle_coordinates = [self.tpolygon.points[idx] for idx in triangle_index]
                triangle_string = ' '.join([f'{point.x*self.scale},{point.y*self.scale}' for point in triangle_coordinates])
                svg_content += f'<polygon points="{triangle_string}" class="red_triangle" opacity="{self.opacity}"/>\n'


        return svg_content

    def _get_edges_svg(self):
        svg_content = ''
        for edge in self.tpolygon.get_edges():
            endpoint1 = edge[0]
            endpoint2 = edge[1]

            x1 = self.tpolygon.get_points()[endpoint1].x * self.scale
            y1 = self.tpolygon.get_points()[endpoint1].y * self.scale
            x2 = self.tpolygon.get_points()[endpoint2].x * self.scale
            y2 = self.tpolygon.get_points()[endpoint2].y * self.scale

            svg_content += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="edge_style" opacity="{self.opacity}"/>\n'

        return svg_content

# Frame que representa a verificação de se um ponto é orelha
# Tpolygon no argumento é o plano de fundo
class VerifyEarFrame(Frame):
    def __init__(self, epolygon, idx, tpolygon=None):
        super().__init__(epolygon)

        if tpolygon != None:
            self.background_svg = TPolygonFrame(tpolygon=tpolygon, opacity=0.2).middle_ground_svg

        self._highlight_verification(idx)
        self._color_ears(epolygon.ear_list)

        self.foreground_svg = self._get_foreground()

    # Colore o triangulo sendo verificado
    def _highlight_verification(self, idx):
        prev_idx = idx-1 if idx>0 else len(self.points)-1
        next_idx = idx+1 if idx<len(self.points)-1 else 0
        self.endpoint1 = prev_idx
        self.endpoint2 = next_idx

        # Vértices sendo verificados ficam em vermelho
        self.set_point_color(prev_idx, "red")
        self.set_point_color(idx, "red")
        self.set_point_color(next_idx, "red")

    # Colore orelhas já vistas de verde
    def _color_ears(self, ear_list):
        # Marca orelhas antigas de azul
        for i in range(len(ear_list)):
            if ear_list[i]:
                self.set_point_color(i, "green")

    # Adiciona uma aresta entre os vizinhos da orelha
    def _get_foreground(self):
        # Aresta de frente
        x1 = self.points[self.endpoint1].x * self.scale
        y1 = self.points[self.endpoint1].y * self.scale
        x2 = self.points[self.endpoint2].x * self.scale
        y2 = self.points[self.endpoint2].y * self.scale

        return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="line_style"/>'

    # Adiciona um tpoylgon no background
    def set_background(self, tpolygon):
        tframe = TPolygonFrame(tpolygon=tpolygon, opacity=0.4)
        self.background_svg += tframe.middle_ground_svg
