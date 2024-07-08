from polygon import Point

# retorna sinal do ângulo entre os segmentos P0P2, P1P2
def angle(Point0, Point1, Point2):
    return (Point0.x - Point2.x)*(Point1.y - Point2.y) - \
           (Point0.y - Point2.y)*(Point1.x - Point2.x)

def in_triangle(Point, triangle):
    signal_1 = angle(Point, triangle[0], triangle[1])
    signal_2 = angle(Point, triangle[1], triangle[2])
    signal_3 = angle(Point, triangle[0], triangle[2])

    return not ((signal_1 > 0 or signal_2 > 0 or signal_3 > 0) and \
            (signal_1 < 0 or signal_2 < 0 or signal_3 < 0))
