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
        self.points_svg = self._get_points()

    def _get_points(self):
        # Desenha os pontos
        svg_content = ''
        for i, point in enumerate(self.points):
            color = self.points_colors[i]
            svg_content += f'<circle cx="{round(point.x*self.scale, 3)}" cy="{round(point.y*self.scale, 3)}" class="{color}_point" opacity="{self.opacity}"/>\n'
        return svg_content

    def _get_middle_ground(self):
        # Cor de fundo do poligono
        points_string = ' '.join([f'{round(point.x*self.scale, 3)},{round(point.y*self.scale, 3)}' for point in self.points])
        return f'<polygon points="{points_string}" class="polygon" opacity="{self.opacity}"/>\n'

    # Todo frame possui cor de fundo para poligono e cor para os pontos
    # Pode adicionar um plano de fundo (ex: polígono triangulado)
    # Pode adicionar um plano de frente (ex: arestas de uma triangulação)
    def generate_svg(self):
        svg_content = f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}">\n'

        # Adiciona os planos
        svg_content += self.background_svg
        svg_content += self.middle_ground_svg
        svg_content += self.foreground_svg
        svg_content += self.points_svg

        svg_content += '</svg>'

        return svg_content
