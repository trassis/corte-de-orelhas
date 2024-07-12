from frame import Frame

# Frame que representa um tpolygon
class TPolygonFrame(Frame):
    def __init__(self, tpolygon, opacity=1.0, color_list=None): 
        super().__init__(polygon=tpolygon, opacity=opacity)

        self.triangle_number = tpolygon.number_of_triangles()
        self.vertex_number = tpolygon.get_size()
        self.tpolygon = tpolygon

        if color_list == None:
            color_list = ["black"] * self.vertex_number

        self.triangles_colors = ["blue"]*self.triangle_number

        self.middle_ground_svg += self._get_edges_svg()
        self.foreground_svg += self._get_foreground()


    def _get_foreground(self):
        svg_content = '' 
        # Desenha triângulos destacados (se houver)
        for i in range(self.triangle_number):
            if self.triangles_colors[i] == "red":
                triangle_string = ' '.join([f'{round(point.x*self.scale, 3)},{round(point.y*self.scale, 3)}' for point in self.tpolygon.get_points()])
                svg_content += f'<polygon points="{triangle_string}" class="red_triangle" opacity="{self.opacity}"/>\n'


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

    def highlight_triangle(self, triangle_idx):
        self.triangles_colors[triangle_idx] = "red"
