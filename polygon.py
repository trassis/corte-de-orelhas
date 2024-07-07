class Polygon:
    def __init__(self, file_name = ''):
        self.size = 0
        self.points = []

        if file_name != '':
            self.read_from_file(file_name)

    def read_from_file(self, file_name):
        self.points = []
        with open(file_name, 'r') as file:
            self.size = int(file.readline().strip())
            for _ in range(self.size):
                x, y = map(int, file.readline().strip().split())
                self.points.append((x,y))
