from polygon import Polygon
from geometry import angle, in_triangle, Point
import frame

class EPolygon(Polygon):
    def __init__(self, file_name='', points=None, ear_list=[], copy_polygon=None):
        super().__init__(file_name=file_name, points=points, copy_polygon=copy_polygon)

        # Preenche a lista de orelhas
        if len(ear_list) == 0:
            self.ear_list = [False]*self.size
        else:
            self.ear_list = ear_list.copy()
        
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
    
    def remove_ear(self):
        ear_index = self.ear_list.index(True)
        new_frames = []

        # Cria polígono sem orelha
        new_epolygon = self.create_new_epolygon(ear_index)

        # Atualiza as orelhas do novo polígono
        previous_index = (ear_index-1) % new_epolygon.get_size()
        next_index = ear_index % new_epolygon.get_size()

        # Computa os frames
        for index in [ previous_index, next_index ]:
            verify_frame = frame.VerifyEarFrame(epolygon=new_epolygon, idx=index)
            new_frames.append(verify_frame)

            new_epolygon.ear_list[index] = new_epolygon.is_ear(index)

            response_frame = frame.VerifyEarFrame(epolygon=new_epolygon, idx=index)
            
            if new_epolygon.ear_list[index]:
                response_frame.set_point_color(index, "red")
            else:
                response_frame.set_point_color(index, "black")

            new_frames.append(response_frame)

        # Pega o triangulo formado e a aresta criada
        new_triangle = self.create_new_triangle(ear_index)
        new_edge = self.create_new_edge(ear_index)

        return [ new_epolygon, new_edge, new_triangle, new_frames ]
    
    # Itera sobre todos os vértices para descobrir se são orelhas
    def ear_verification_frames(self):
        if len(self.points) != len(self.ear_list):
            raise ValueError(len(self.points), len(self.ear_list))

        frames = []
        for i in range(self.size):
            verify_frame = frame.VerifyEarFrame(epolygon=self, idx=i)
            frames.append(verify_frame)

            response_frame = frame.VerifyEarFrame(epolygon=self, idx=i)

            if self.is_ear(i):
                self.ear_list[i] = True
                response_frame.set_point_color(i, "green")
            else:
                response_frame.set_point_color(i, "black")

            frames.append(response_frame)

        return frames

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
    
