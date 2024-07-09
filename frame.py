from polygon import Polygon

class Frame:
 
    def __init__(self, polygon, ear_list):
        if not isinstance(polygon, Polygon):
            raise TypeError("Object polygon should be of class Polygon")

        if polygon.get_size() != len(ear_list):
            raise ValueError("Polygon and list should be of the same size")

        self.polygon = polygon
        self.vertex_type = ["black"]*polygon.get_size()
        # Marca orelhas antigas de azul
        for i in range(len(ear_list)):
            if ear_list[i]:
                self.set_vertex_type(i, "blue")
        
        self.scale = 20

    def set_vertex_type(self, idx, new_type):
        if idx >= len(self.vertex_type):
            raise IndexError("Índice fora da lista")
        self.vertex_type[idx] = new_type

    def generate_svg(self):
        # Create the polygon element
        svg_content = []
        points_string = ' '.join([f'{point.x*self.scale},{point.y*self.scale}' for point in self.polygon.points])
        svg_content.append(f'<polygon points="{points_string}" class="polygon"/>')
        
        # Create circles for each vertex with corresponding classes
        for i, point in enumerate(self.polygon.points):
            vertex_class = self.vertex_type[i]
            svg_content.append(f'<circle cx="{point.x*self.scale}" cy="{point.y*self.scale}" r="5" class="{vertex_class}_point"/>')

        return svg_content

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

    def generate_svg(self):
        svg_content = super().generate_svg()
        x1 = self.polygon.points[self.endpoint1].x * self.scale
        y1 = self.polygon.points[self.endpoint1].y * self.scale
        x2 = self.polygon.points[self.endpoint2].x * self.scale
        y2 = self.polygon.points[self.endpoint2].y * self.scale
        svg_content.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="line_style"/>')

        return svg_content

class Neighbor_Frame(Frame):
    def generate_svg(self):
        pass


