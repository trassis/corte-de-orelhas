from frame import Frame
from tframe import TPolygonFrame
from epolygon import EPolygon

# Frame que mostra orelhas em verde, e possui tpolygon de plano de fundo
# Deixa colorir um ponto idx com a cor color
class EarFrame(Frame):
    def __init__(self, epolygon, idx=-1, color="black"):
        points_colors = self._get_points_colors(epolygon.ear_list)
        if idx != -1:
            points_colors[idx] = color
        super().__init__(polygon=epolygon, points_colors=points_colors)

    def _get_points_colors(self, ear_list):
        points_colors = ["black"] * len(ear_list)
        for i in range(len(ear_list)):
            if ear_list[i]:
                points_colors[i] = "green"
        return points_colors

    # Adiciona um tpoylgon no background
    def set_background(self, tpolygon):
        tframe = TPolygonFrame(tpolygon=tpolygon, opacity=0.4)
        self.background_svg += tframe.middle_ground_svg

# Frame vazio, só com plano de fundo
class EmptyEarFrame(EarFrame):
    def __init__(self):
        super().__init__(epolygon=EPolygon(points=[]))

# Frame que representa a verificação de se um ponto é orelha
class VerifyEarFrame(EarFrame):
    def __init__(self, epolygon, idx, color):
        super().__init__(epolygon=epolygon, idx=idx, color=color)
        self._draw_red_edge(idx)

    # Desenha uma aresta entre os vizinhos do ponto idx
    def _draw_red_edge(self, idx):
        prev_idx = idx-1 if idx>0 else len(self.points)-1
        next_idx = idx+1 if idx<len(self.points)-1 else 0

        x1 = self.points[prev_idx].x * self.scale
        y1 = self.points[prev_idx].y * self.scale
        x2 = self.points[next_idx].x * self.scale
        y2 = self.points[next_idx].y * self.scale

        self.foreground_svg += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="line_style"/>'
