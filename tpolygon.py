class TPolygon:
    def __init__(self, polygon, new_edges, triangles):
        self.polygon = polygon
        self.new_edges = new_edges
        self.triangles = triangles

    def number_of_triangles(self):
        return self.polygon.get_size() - 2
    
    def number_of_vertices(self):
        return self.polygon.get_size()

    def vertices_of_triangle(self, idx):
        return self.triangles[idx]

    # quem ta em v mas não esta u
    def subtract_neighbors(self, v, u):
        ret = []
        for i in self.vertices_of_triangle(v):
            ok = True
            for j in self.vertices_of_triangle(u):
                if i == j:
                    ok = False
            if ok:
                ret.append(i)

        if len(ret) != 1:
            raise ValueError("This should be only one!")

        return ret[0]

    def get_points(self):
        return self.polygon.get_points()
    
    def get_edges(self):
        return self.new_edges
    
    def is_adj(self, t1, t2):
        pontos_comuns = set(t1) & set(t2)
        return len(pontos_comuns) == 2

    def neighbors(self, idx):
        neib = []

        for i in range(len(self.triangles)):
            if i == idx: 
                continue
            if self.is_adj(self.triangles[i], self.triangles[idx]):
                neib.append(i)
                
        return neib
            
    def generate_html(self):
        # Sem background por enquanto
        """
        frame.clear_frames()

        zero_list = [ 0 ]* self.polygon_list[0].get_size()
        background_frame = frame.Triangle_Frame(self.get_result(), zero_list, self.frame_options, 0.2)
        """

        with open(f"./frames/frame{i}.svg", "w") as file:
            file.write(frame.generate_svg(None))

        return html_generator.get(len(self.frame_list), self.frame_options.width, self.frame_options.height)
