from frame import Frame

# Frame que representa um tpolygon
# Cor dos vértices dada por color_list
# Pode destacar um triângulo idx
class TPolygonFrame(Frame):
    def __init__(self, tpolygon, opacity=1.0, points_colors=[], idx=-1, description=''): 
        super().__init__(polygon=tpolygon, points_colors=points_colors, opacity=opacity, description=description)

        self.triangle_number = tpolygon.number_of_triangles()
        self.vertex_number = tpolygon.get_size()
        self.tpolygon = tpolygon

        self.triangles_colors = ["black"]*self.triangle_number
        if idx != -1:
            self.triangles_colors[idx] = "red"

        self.middle_ground_svg += self._get_edges_svg()
        self.foreground_svg += self._get_foreground()

    # Desenha triângulos destacados (se houver)
    def _get_foreground(self):
        svg_content = '' 
        for i in range(self.triangle_number):
            if self.triangles_colors[i] == "red":
                indices = self.tpolygon.vertices_of_triangle(i)
                points = [ self.tpolygon.points[i] for i in indices ]
                triangle_string = ' '.join([f'{round(point.x*self.scale, 3)},{round(point.y*self.scale, 3)}' for point in points ])
                svg_content += f'<polygon points="{triangle_string}" class="highlight_polygon" opacity="{self.opacity}"/>\n'

        return svg_content

    def _get_edges_svg(self):
        svg_content = ''
        for edge in self.tpolygon.get_edges():
            endpoint1 = edge[0]
            endpoint2 = edge[1]

            x1 = round(self.tpolygon.get_points()[endpoint1].x * self.scale, 3)
            y1 = round(self.tpolygon.get_points()[endpoint1].y * self.scale, 3)
            x2 = round(self.tpolygon.get_points()[endpoint2].x * self.scale, 3)
            y2 = round(self.tpolygon.get_points()[endpoint2].y * self.scale, 3)

            svg_content += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="edge_style" opacity="{self.opacity}"/>\n'

        return svg_content
