import wx

CELL_WIDTH = 50
CELL_HEIGHT = 50
TOP_MARGIN = 10
RIGHT_MARGIN = 10
BOTTOM_MARGIN = 30
LEFT_MARGIN = RIGHT_MARGIN

CONTROLS_WIDTH = 100

AGENT_RADIUS = 5
AGENT_BASE_COLOR = '#000000'
TERRITORY_BORDER_COLOR = '#eeeeee'


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
        self.populationSize = size
        self.size = (size[0] + CONTROLS_WIDTH, size[1])
        super(PopulationVisualizerFrame, self).__init__(parent, title=title, size=self.size)
        self.population = population
        self.InitUI()
        self.Show(True)

    def InitUI(self):
        self.panel = wx.Panel(self)
        simulateButton = wx.Button(self.panel, label='Simulate', pos=(self.size[0] - CONTROLS_WIDTH, 10))
        self.Bind(wx.EVT_BUTTON, self.draw, simulateButton)
        stopButton = wx.Button(self.panel, label='Stop', pos=(self.size[0] - CONTROLS_WIDTH, 40))
        self.Bind(wx.EVT_BUTTON, self.stop, stopButton)
        self.buffer = wx.EmptyBitmap(self.populationSize[0], self.populationSize[1])

    def draw(self, e):
        self.timer = wx.Timer(self)
        self.timer.Start(1000)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        dc = wx.BufferedDC(wx.ClientDC(self.panel), self.buffer)
        self.drawAnimals(dc)

    def update(self, event):
        if self.timer.IsRunning():
            self.population.simulate_one_unit_of_time(0.2)
            dc = wx.BufferedDC(wx.ClientDC(self.panel), self.buffer)
            self.drawAnimals(dc)

    def drawAnimals(self, dc):
        dc.Clear()
        self.drawTerritory(dc)
        dc.SetBrush(wx.Brush(AGENT_BASE_COLOR))
        for animal in self.population.animals:
            x_start = LEFT_MARGIN + animal.x*CELL_WIDTH
            y_start = TOP_MARGIN + animal.y*CELL_HEIGHT
            dc.DrawCircle(x_start, y_start, AGENT_RADIUS)

    def drawTerritory(self, dc):
        dc.SetBrush(wx.Brush(TERRITORY_BORDER_COLOR))
        rect_size = (self.populationSize[0] - RIGHT_MARGIN - LEFT_MARGIN,
                     self.populationSize[1] - BOTTOM_MARGIN - TOP_MARGIN)
        dc.DrawRectangle(RIGHT_MARGIN, TOP_MARGIN, rect_size[0], rect_size[1])

        # for i in range(LEFT_MARGIN + CELL_WIDTH, self.populationSize[0] - LEFT_MARGIN, CELL_WIDTH):
        #     dc.DrawLine(i, TOP_MARGIN, i, TOP_MARGIN + rect_size[1])
        #
        # for i in range(TOP_MARGIN + CELL_HEIGHT, self.populationSize[1] - BOTTOM_MARGIN, CELL_HEIGHT):
        #     dc.DrawLine(LEFT_MARGIN, i, LEFT_MARGIN + rect_size[0], i)

    def stop(self, event):
        if not self.timer is None and self.timer.IsRunning():
            self.timer.Stop()
