import frame
from geometry import angle, in_triangle, Point

class Polygon:
    def __init__(self, file_name='', points=None, ear_list=[]):
        if points is None:
            self.size = 0
            self.points = []
        else:
            self.size = len(points)
            self.points = points

        # MUDAR CONSTRUTOR para aqui também funcionar com .pol
        if file_name != '':
            self.read_from_file(file_name)

        if len(ear_list) == 0:
            self.ear_list = [False]*self.size
        else:
            self.ear_list = ear_list.copy()

        if len(self.points) != len(self.ear_list):
            raise ValueError(len(self.points), len(self.ear_list))


    # Obtem um poligono representado em um arquivo
    def read_from_file(self, file_name):
        self.points = []
        with open(file_name, 'r') as file:
            self.size = int(file.readline().strip())
            for i in range(self.size):
                x, y = map(int, file.readline().strip().split())
                self.points.append(Point(x,y,i))

    def read_from_pol(self, file_path):
        self.points = []
        with open(file_path, 'r') as file:
            line = file.readline().strip()

            # Split the line into parts
            parts = line.split()

            # The first part is N
            N = int(parts[0])
            self.size = N

            # The remaining parts are coordinates
            coordinates = parts[1:]

            # Ensure there are the correct number of coordinate pairs
            if len(coordinates) != 2 * N:
                raise ValueError(f"Expected {2 * N} coordinate parts, but got {len(coordinates)}")

            for i in range(N):
                p, q = map(int, coordinates[2 * i].split('/'))
                r, s = map(int, coordinates[2 * i + 1].split('/'))
                x = p / q
                y = r / s
                self.points.append(Point(x, y, i))

        self.ear_list = [False]*self.size


    def get_size(self):
        return self.size

    # Retorna se o ponto no índice idx é uma orelha
    def is_ear(self, idx):
        if self.size <= 3:
            return False

        previous_idx = idx-1 if idx>0 else self.size-1
        next_idx = idx+1 if idx+1 < self.size else 0

        # Verifica se o angulo entre os pontos é a esquerda
        if angle(self.points[previous_idx], self.points[idx], self.points[next_idx]) <= 0:
            return False

        # Verifica se há algum ponto dentro do triangulo
        triangle = [ self.points[previous_idx], self.points[idx], self.points[next_idx] ]
        for i, point in enumerate(self.points):
            if i == previous_idx or i == idx or i == next_idx:
                continue
            if in_triangle(point, triangle):
                return False

        return True

    # Itera sobre todos os vértices para descobrir se são orelhas
    def ear_verification_frames(self, frame_options):
        if len(self.points) != len(self.ear_list):
            raise ValueError(len(self.points), len(self.ear_list))

        frames = []
        for i in range(self.size):
            verify_frame = frame.Ear_Frame(self, self.ear_list, frame_options, i)
            frames.append(verify_frame)

            response_frame = frame.Ear_Frame(self, self.ear_list, frame_options, i)

            if self.is_ear(i):
                self.ear_list[i] = True
                response_frame.set_vertex_type(i, "green")
            else:
                response_frame.set_vertex_type(i, "black")

            frames.append(response_frame)

        return frames

    # Retorna um novo polígono a partir da remoção de uma orelha do atual
    # Retorna a nova aresta
    # Retorna o novo triangulo
    # Retorna os frames gerados no processo
    # O novo polígono possui lista de orelhas já pronta
    def remove_ear(self, frame_options):
        ear_index = self.ear_list.index(True)
        new_frames = []

        # Novo polígono
        new_ear_list = self.ear_list.copy()
        new_ear_list.pop(ear_index)
        new_points = []
        for pt in self.points:
            new_points.append(Point(pt.x, pt.y, pt.idx))
        new_points.pop(ear_index)
        new_polygon = Polygon(points=new_points, ear_list=new_ear_list)

        # Atualiza as orelhas do novo polígono
        previous_index = (ear_index-1) % new_polygon.get_size()
        next_index = ear_index % new_polygon.get_size()
        for index in [ previous_index, next_index ]:
            verify_frame = frame.Ear_Frame(new_polygon, new_polygon.ear_list, frame_options, index)
            new_frames.append(verify_frame)

            new_polygon.ear_list[index] = new_polygon.is_ear(index)

            response_frame = frame.Ear_Frame(new_polygon, new_polygon.ear_list, frame_options, index)
            if new_polygon.ear_list[index]:
                response_frame.set_vertex_type(index, "red")
            else:
                response_frame.set_vertex_type(index, "black")

            new_frames.append(response_frame)

        # Nova aresta e novo triangulo
        index1 = self.points[(ear_index-1) % self.get_size()].idx
        index2 = self.points[(ear_index) % self.get_size()].idx
        index3 = self.points[(ear_index+1) % self.get_size()].idx

        new_edge = [index1, index3]
        new_triangle = [index1, index2, index3]

        return [ new_polygon, new_edge, new_triangle, new_frames ]

    def add_vertex(self, Point):
        self.size += 1
        self.points.append(Point)

    def removed_vertex(self, idx):
        new_points = []
        for i, pt in enumerate(self.points):
            if i != idx:
                new_points.append(Point(pt.x, pt.y, pt.idx))
        return Polygon('', new_points)
    
    def get_points(self):
        return self.points
