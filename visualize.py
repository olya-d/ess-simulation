import wx
import simulation

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
    def __init__(self):
        self.app = wx.App()
        self.frame = SettingsFrame()

    def show(self):
        self.app.MainLoop()


class SettingsFrame(wx.Frame):

    def __init__(self):
        self.title = 'Settings | ESS'
        wx.Frame.__init__(self, wx.GetApp().TopWindow, title=self.title, size=(400, 300))
        self.InitUI()
        self.Show()

    def InitUI(self):
        panel = wx.Panel(self)
        v_sizer = wx.BoxSizer(wx.VERTICAL)

        # Speed
        h_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        st_speed = wx.StaticText(panel, label='Speed of movement:')
        self.tc_speed = wx.TextCtrl(panel, -1, "0.2")
        h_sizer1.Add(st_speed, flag=wx.RIGHT, border=8)
        h_sizer1.Add(self.tc_speed, proportion=1)
        v_sizer.Add(h_sizer1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # Size
        h_sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        st_size = wx.StaticText(panel, label='Size of population:')
        self.tc_size = wx.TextCtrl(panel, -1, "100")
        h_sizer2.Add(st_size, flag=wx.RIGHT, border=8)
        h_sizer2.Add(self.tc_size, proportion=1)
        v_sizer.Add(h_sizer2, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # Density
        h_sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        st_density = wx.StaticText(panel, label='Density of population:')
        self.tc_density = wx.TextCtrl(panel, -1, "1")
        h_sizer2.Add(st_density, flag=wx.RIGHT, border=8)
        h_sizer2.Add(self.tc_density, proportion=1)
        v_sizer.Add(h_sizer2, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # Life span
        h_sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        st_lifeSpan = wx.StaticText(panel, label='Life span:')
        self.tc_lifeSpan = wx.TextCtrl(panel, -1, "20")
        h_sizer2.Add(st_lifeSpan, flag=wx.RIGHT, border=8)
        h_sizer2.Add(self.tc_lifeSpan, proportion=1)
        v_sizer.Add(h_sizer2, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # Simulate button
        v_sizer.Add((-1, 25))
        h_sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        simulateButton = wx.Button(panel, label='Simulate')
        h_sizer2.Add(simulateButton, flag=wx.LEFT | wx.BOTTOM, border=5)
        v_sizer.Add(h_sizer2, flag=wx.ALIGN_CENTER | wx.RIGHT, border=10)

        panel.SetSizer(v_sizer)

        self.Bind(wx.EVT_BUTTON, self.openSimulation, simulateButton)

    def openSimulation(self, event):
        game = simulation.Game([[(-8, -8), (-6, 10)], [(10, -6), (-1, -1)]])
        size = int(self.tc_size.GetValue())
        life_span = int(self.tc_lifeSpan.GetValue())
        density = float(self.tc_density.GetValue())
        self.population = simulation.Population(game, size, life_span=life_span, density=density)
        self.population.generate()
        PopulationVisualizerFrame(None, 'ESS', self.population, float(self.tc_speed.GetValue()))


class PopulationVisualizerFrame(wx.Frame):
    def __init__(self, parent, title, population, speed):
        simulationSize = (population.territory.width*CELL_WIDTH + LEFT_MARGIN + RIGHT_MARGIN,
                          population.territory.height*CELL_HEIGHT + TOP_MARGIN + BOTTOM_MARGIN)
        size = (simulationSize[0] + CONTROLS_WIDTH, simulationSize[1])
        super(PopulationVisualizerFrame, self).__init__(parent, title=title, size=size)
        self.simulationSize = simulationSize
        self.population = population
        self.speed = speed
        self.InitUI()
        self.Show(True)

    def InitUI(self):
        self.panel = wx.Panel(self)
        w, h = self.GetClientSize()

        self.SetMenuBar(wx.MenuBar())

        self.continueButton = wx.Button(self.panel, label='Continue', pos=(w - CONTROLS_WIDTH, TOP_MARGIN))
        self.Bind(wx.EVT_BUTTON, self.draw, self.continueButton)

        self.stopButton = wx.Button(self.panel, label='Stop',
                                    pos=(w - CONTROLS_WIDTH, wx.Button_GetDefaultSize()[1] + SPACE_BETWEEN_CONTROLS))
        self.Bind(wx.EVT_BUTTON, self.stop, self.stopButton)

        self.buffer = wx.EmptyBitmap(self.simulationSize[0], self.simulationSize[1])

        # Population statistics
        self.statusBar = self.CreateStatusBar()

        self.draw(None)

    def draw(self, event):
        self.continueButton.Disable()
        self.stopButton.Enable()
        self.timer = wx.Timer(self)
        self.timer.Start(500)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        dc = wx.BufferedDC(wx.ClientDC(self.panel), self.buffer)
        self.drawAnimals(dc)

    def update(self, event):
        if self.timer.IsRunning():
            self.population.simulate_one_unit_of_time(self.speed)
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
        self.continueButton.Enable()
        self.stopButton.Disable()
