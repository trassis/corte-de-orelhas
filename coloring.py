from queue import Queue
from frame import TPolygonFrame
from html_generator import clear_frames
import html_generator 

class Coloring:
    def __init__(self, tpolygon):
        self.polygon = tpolygon
        self.n = tpolygon.number_of_triangles()

    
        self.color = [0]*self.polygon.get_size()
        self.frame_list = []

    def solve(self):
        vis = [False]*self.n

        initial_frame = TPolygonFrame(tpolygon=self.polygon, color_list =self.color)
        self.frame_list.append(initial_frame)

        q = Queue()
        q.put(0)
        vis[0] = True

        x,y,z = self.polygon.vertices_of_triangle(0) 
        self.color[x] = 1
        self.color[y] = 2
        self.color[z] = 3

        while not q.empty():
            v = q.get()
            for u in self.polygon.neighbors(v):
                if not vis[u]:
                    vis[u] = True
                    q.put(u)

                    red_frame = TPolygonFrame(tpolygon=self.polygon, color_list =self.color, idx = u)
                    self.frame_list.append(red_frame)

                    only_in_v = self.polygon.subtract_neighbors(v, u)
                    not_colored = self.polygon.subtract_neighbors(u, v)
                    self.color[not_colored] = self.color[only_in_v]

                    colored_frame = TPolygonFrame(tpolygon=self.polygon, color_list =self.color)
                    self.frame_list.append(colored_frame)
