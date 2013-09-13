import wx

CELL_WIDTH = 50
CELL_HEIGHT = 50
TOP_MARGIN = 10
RIGHT_MARGIN = 10
BOTTOM_MARGIN = 30
AGENT_RADIUS = 5
LEFT_MARGIN = RIGHT_MARGIN


class PopulationVisualizer():
    def __init__(self, population):
        self.app = wx.App()
        width = population.territory.width * CELL_WIDTH + LEFT_MARGIN + RIGHT_MARGIN
        height = population.territory.height * CELL_HEIGHT + TOP_MARGIN + BOTTOM_MARGIN
        self.frame = PopulationVisualizerFrame(None, 'ESS', population, (width, height))

    def show(self):
        self.app.MainLoop()


class PopulationVisualizerFrame(wx.Frame):
    def __init__(self, parent, title, population, size=(800, 600)):
        super(PopulationVisualizerFrame, self).__init__(parent, title=title, size=size)
        print(size)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.population = population
        self.size = size
        self.Show()

    def OnPaint(self, e):
        dc = wx.PaintDC(self)
        dc.SetPen(wx.Pen('#333333'))

        # Territory
        # dc.DrawRectangle(10, 10, 780, 560)
        rect_size = (self.size[0] - RIGHT_MARGIN - LEFT_MARGIN, self.size[1] - BOTTOM_MARGIN - TOP_MARGIN)
        dc.DrawRectangle(RIGHT_MARGIN, TOP_MARGIN, rect_size[0], rect_size[1])

        for i in range(LEFT_MARGIN + CELL_WIDTH, self.size[0] - LEFT_MARGIN, CELL_WIDTH):
            dc.DrawLine(i, TOP_MARGIN, i, TOP_MARGIN + rect_size[1])

        for i in range(TOP_MARGIN + CELL_HEIGHT, self.size[1] - BOTTOM_MARGIN, CELL_HEIGHT):
            dc.DrawLine(LEFT_MARGIN, i, LEFT_MARGIN + rect_size[0], i)

        dc.SetBrush(wx.Brush('#222222'))
        for animal in self.population.animals:
            x_start = LEFT_MARGIN + animal.x * CELL_WIDTH
            y_start = TOP_MARGIN + animal.y * CELL_HEIGHT
            dc.DrawCircle(x_start, y_start, AGENT_RADIUS)
