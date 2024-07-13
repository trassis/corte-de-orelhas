class FrameOptions:
    height = 700
    width = 500
    scale = 5

    @classmethod
    def set(cls, polygon, width, height):
        cls.width = width
        cls.height = height

        xlim = 0
        ylim = 0
        for point in polygon.points:
            xlim = max(xlim, point.x)
            ylim = max(ylim, point.y)
        xlim *= 1.05 
        ylim *= 1.05 
        cls.scale = min(width/xlim, height/ylim)
