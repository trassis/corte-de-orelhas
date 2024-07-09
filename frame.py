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

    def set_vertex_type(self, idx, new_type):
        if idx >= len(self.vertex_type):
            raise IndexError("Índice fora da lista")
        self.vertex_type[idx] = new_type

    def generate_svg(self):
        raise NotImplementedError("Subclass must implement abstract method")

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
        pass

class Neighbor_Frame(Frame):
    def generate_svg(self):
        pass
