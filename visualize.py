import wx

CELL_WIDTH = 50
CELL_HEIGHT = 50
TOP_MARGIN = 10
RIGHT_MARGIN = 10
BOTTOM_MARGIN = 50
LEFT_MARGIN = RIGHT_MARGIN

CONTROLS_WIDTH = 100
SPACE_BETWEEN_CONTROLS = 20

AGENT_RADIUS = 10
AGENT_BASE_COLOR = '#000000'
TERRITORY_BORDER_COLOR = '#eeeeee'
STRATEGY_COLORS = ['#0B62A4', '#FF9F01', '#0000ff']
INTERACTION_COLOR = '#ffffff'


class PopulationVisualizer():
    def __init__(self, population):
        self.app = wx.App()
        width = population.territory.width * CELL_WIDTH + LEFT_MARGIN + RIGHT_MARGIN
        height = population.territory.height * CELL_HEIGHT + TOP_MARGIN + BOTTOM_MARGIN
        self.frame = PopulationVisualizerFrame(None, 'ESS', population, (width, height))

    def show(self):
        self.app.MainLoop()


class PopulationVisualizerFrame(wx.Frame):
    def __init__(self, parent, title, population, simulationSize=(800, 600)):
        size = (simulationSize[0] + CONTROLS_WIDTH, simulationSize[1])
        super(PopulationVisualizerFrame, self).__init__(parent, title=title, size=size)
        self.simulationSize = simulationSize
        self.population = population
        self.InitUI()
        self.Show(True)

    def InitUI(self):
        self.panel = wx.Panel(self)
        w, h = self.GetClientSize()

        self.SetMenuBar(wx.MenuBar())

        self.simulateButton = wx.Button(self.panel, label='Simulate', pos=(w - CONTROLS_WIDTH, TOP_MARGIN))
        self.Bind(wx.EVT_BUTTON, self.draw, self.simulateButton)

        self.stopButton = wx.Button(self.panel, label='Stop',
                               pos=(w - CONTROLS_WIDTH, wx.Button_GetDefaultSize()[1] + SPACE_BETWEEN_CONTROLS))
        self.Bind(wx.EVT_BUTTON, self.stop, self.stopButton)
        self.stopButton.Disable()

        # Label for text box
        pos = (w - CONTROLS_WIDTH, wx.Button_GetDefaultSize()[1]*2 + SPACE_BETWEEN_CONTROLS*2)
        size = (CONTROLS_WIDTH, wx.Button_GetDefaultSize()[1])
        wx.StaticText(self.panel, label='Speed', pos=pos, size=size)
        # Text box for speed of movement
        pos = (w - CONTROLS_WIDTH, wx.Button_GetDefaultSize()[1]*3 + SPACE_BETWEEN_CONTROLS*2)
        size = (wx.Button_GetDefaultSize()[0], wx.Button_GetDefaultSize()[1])
        self.speedTextCtrl = wx.TextCtrl(self.panel, -1, '0.2', pos=pos, size=size)
        self.buffer = wx.EmptyBitmap(self.simulationSize[0], self.simulationSize[1])

        # Population statistics
        self.statusBar = self.CreateStatusBar()

    def draw(self, e):
        self.simulateButton.Disable()
        self.stopButton.Enable()
        self.timer = wx.Timer(self)
        self.timer.Start(500)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        dc = wx.BufferedDC(wx.ClientDC(self.panel), self.buffer)
        self.drawAnimals(dc)

    def update(self, event):
        if self.timer.IsRunning():
            self.population.simulate_one_unit_of_time(float(self.speedTextCtrl.GetValue()))
            dc = wx.BufferedDC(wx.ClientDC(self.panel), self.buffer)
            self.drawAnimals(dc)

    def drawAnimals(self, dc):
        dc.Clear()
        self.drawTerritory(dc)
        countStrategy0 = 0
        for animal in self.population.animals:
            x_start = LEFT_MARGIN + animal.x*CELL_WIDTH
            y_start = TOP_MARGIN + animal.y*CELL_HEIGHT
            if animal.interacting_with is None:
                dc.SetBrush(wx.Brush(STRATEGY_COLORS[animal.strategy]))
            else:
                dc.SetBrush(wx.Brush(INTERACTION_COLOR))
            dc.DrawCircle(x_start, y_start, AGENT_RADIUS)
            score = str(animal.score)
            tw, th = dc.GetTextExtent(score)
            # dc.SetFont(wx.wxFont(12, wxMODERN, wxNORMAL, wxNORMAL))
            dc.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL))
            dc.DrawText(score, x_start - tw/2, y_start - th/2)
            if animal.strategy == 0:
                countStrategy0 += 1
        statusText = "Strategy 1 : Strategy 2 = %d : %d" % (countStrategy0, (self.population.size - countStrategy0))
        self.statusBar.SetStatusText(statusText)


    def drawTerritory(self, dc):
        dc.SetBrush(wx.Brush(TERRITORY_BORDER_COLOR))
        rect_size = (self.simulationSize[0] - RIGHT_MARGIN - LEFT_MARGIN,
                     self.simulationSize[1] - BOTTOM_MARGIN - TOP_MARGIN)
        dc.DrawRectangle(RIGHT_MARGIN, TOP_MARGIN, rect_size[0], rect_size[1])

    def stop(self, event):
        if not self.timer is None and self.timer.IsRunning():
            self.timer.Stop()
        self.simulateButton.Enable()
        self.stopButton.Disable()
