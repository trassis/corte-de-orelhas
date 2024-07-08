
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def angle(p1, p2, p3) :
    return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y);


def in_triangle (pt, triangle):

    signal1 = angle(pt, triangle[0], triangle[1]);
    signal2 = angle(pt, triangle[1], triangle[2]);
    signal3 = angle(pt, triangle[2], triangle[0]);

    has_neg = (signal1 < 0) or (signal2 < 0) or (signal3 < 0);
    has_pos = (signal1 > 0) or (signal2 > 0) or (signal3 > 0);

    return not(has_neg and has_pos);

