from geometry import angle, in_triangle, Point


class Polygon:
    def __init__(self, file_name='', points=None):
        if points is None:
            self.size = 0
            self.points = []
        else:
            self.size = len(points)
            self.points = points

        if file_name != '':
            self.read_from_file(file_name)
        

    # Obtem um poligono representado em um arquivo
    def read_from_file(self, file_name):
        self.points = []
        with open(file_name, 'r') as file:
            self.size = int(file.readline().strip())
            for _ in range(self.size):
                x, y = map(int, file.readline().strip().split())
                self.points.append(Point(x,y))

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
                self.points.append(Point(x, y))


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

    def add_vertex(self, Point):
        self.size += 1
        self.points.append(Point)

    def removed_vertex(self, idx):
        new_points = []
        for i, pt in enumerate(self.points):
            if i != idx:
                new_points.append(Point(pt.x, pt.y))
        return Polygon('', new_points)
