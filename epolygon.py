from polygon import Polygon
from geometry import angle, in_triangle, Point
from eframe import VerifyEarFrame, EarFrame

class EPolygon(Polygon):
    def __init__(self, file_name='', points=None, ear_list=[], copy_polygon=None):
        super().__init__(file_name=file_name, points=points, copy_polygon=copy_polygon)

        # Preenche a lista de orelhas
        if len(ear_list) == 0:
            self.ear_list = [False]*self.size
        else:
            self.ear_list = ear_list.copy()
        
    # Retorna se o ponto idx é uma orelha
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

    # Atualiza a lista de orelhas nessa posição e gera frames
    def update_ear_list(self, idx):
        frames = []
        verify_frame = VerifyEarFrame(epolygon=self, idx=idx, color="red")
        frames.append(verify_frame)

        response_frame = None
        if self.is_ear(idx):
            response_frame = VerifyEarFrame(epolygon=self, idx=idx, color="green")
            self.ear_list[idx] = True
        else:
            response_frame = VerifyEarFrame(epolygon=self, idx=idx, color="black")
            self.ear_list[idx] = False 

        frames.append(response_frame)

        return frames

    # Encontra uma orelha e remove ela
    def remove_ear(self):
        ear_index = self.ear_list.index(True)

        new_frames = []

        removal_frame = EarFrame(self, idx=ear_index, color="red")
        new_frames.append(removal_frame)

        # Cria polígono sem orelha
        new_epolygon = self.create_new_epolygon(ear_index)

        # Atualiza as orelhas do novo polígono
        previous_index = (ear_index-1) % new_epolygon.get_size()
        next_index = ear_index % new_epolygon.get_size()
        for index in [ previous_index, next_index ]:
            new_frames += new_epolygon.update_ear_list(index)

        # Pega o triangulo formado e a aresta criada
        new_triangle = self.create_new_triangle(ear_index)
        new_edge = self.create_new_edge(ear_index)

        return [ new_epolygon, new_edge, new_triangle, new_frames ]

    # Cria um polígono sem a orelha especificada
    def create_new_epolygon(self, ear_index):
        new_ear_list = self.ear_list.copy()
        new_ear_list.pop(ear_index)

        new_points = []
        for pt in self.points:
            new_points.append(Point(pt.x, pt.y, pt.idx))
        new_points.pop(ear_index)

        return EPolygon(points=new_points, ear_list=new_ear_list)
    
    # Novo triangulo
    def create_new_triangle(self, ear_index):
        index1 = self.points[(ear_index-1) % self.get_size()].idx
        index2 = self.points[(ear_index) % self.get_size()].idx
        index3 = self.points[(ear_index+1) % self.get_size()].idx

        new_triangle = [index1, index2, index3]

        return new_triangle
    
    # Nova aresta
    def create_new_edge(self, ear_index):
        # Nova aresta e novo triangulo
        index1 = self.points[(ear_index-1) % self.get_size()].idx
        index3 = self.points[(ear_index+1) % self.get_size()].idx

        new_edge = [index1, index3]

        return new_edge
    
