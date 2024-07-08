from geometry import angle, in_triangle


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
                self.points.append((x,y))

    # Retorna se o ponto no índice idx é uma orelha
    def is_ear(self, idx):
        if self.size < 3:
            return False

        previous_point = self.points[idx-1]
        point = self.points[idx]
        next_point = self.points[idx+1]

        # Verifica se o angulo entre os pontos é a esquerda
        if angle(previous_point, point, next_point) > 0:
            return False

        # Verifica se há algum ponto dentro do triangulo
        triangle = [ previous_point, point, next_point ]
        for point in self.points:
            if in_triangle(point, triangle):
                return False

        return True

    def add_point(self, Point):
        self.size += 1
        self.points.append(Point)

    def remove_vertex(self, idx):
        return self.points.remove(idx)
