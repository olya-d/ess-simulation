import random
import visualize
import math


def greatest_pair_of_factors(n):
    """
    Finds pair of integers (a, b) such as a*b = n and
    there is no such (c, d) that c*d=n and |c-d| < |a-b|.
    It basically finds the closest integer representation of square root.
    Examples:
    greatest_pair_of_factors(5) >> (1, 5)
    greatest_pair_of_factors(20) >> (4, 5)
    """
    pairs = []
    factor = 1
    while factor * factor <= n:
        if n % factor == 0:
            pairs.append((n / factor, factor))
        factor += 1
    greatest = pairs[0]
    for pair in pairs:
        if abs(pair[0] - pair[1]) < abs(greatest[0] - greatest[1]):
            greatest = pair
    return greatest


class Territory(object):
    """
    Represents a territory, where animals live.
    Initializes with an empty map
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = [[[] for i in xrange(width)] for j in xrange(height)]

    def is_point_inside(self, x, y):
        return 0 < x < self.width and 0 < y < self.height

    def is_cell_occupied(self, i, j):
        return self.map[i][j] is []

    def occupy_cell(self, x, y, agent):
        """
        Occupies one cell for the map (integer)
        Records (x, y) for animal (float)
        """
        j = x
        i = int(round(y) - 0.5)
        self.map[i][j].append(agent)
        agent.x = j + random.random()
        agent.y = i + random.random()

    def get_agents_in_cell(self, i, j):
        return self.map[i][j]

    def populate(self, agents, density):
        """
        Populates the territory with agents with population density.
        It calculates the square, in which one agent lives.
        """
        agents = agents[:]
        for_one_agent = 1.0 / density
        x = 0
        while x < self.width:
            y = for_one_agent
            while y <= self.height:
                self.occupy_cell(x, y, agents.pop())
                y += for_one_agent
            x += 1


class Animal(object):
    """
    Represents an animal.
    Basic class for different behaviours
    """

    def __init__(self, territory):
        self.territory = territory
        self.x = 0
        self.y = 0

    def move(self, speed):
        """
        Moves in random direction with speed
        """
        if speed > self.territory.width and speed > self.territory.height:
            return
        angle = random.random()*360
        dx = speed*math.cos(angle*math.pi/180)
        dy = speed*math.sin(angle*math.pi/180)
        new_x = self.x + dx
        new_y = self.y + dy
        if self.territory.is_point_inside(new_x, new_y):
            self.x, self.y = new_x, new_y
        else:
            self.move(speed)


class Population(object):
    """
    Represents a population, consisted of animals (Animal class).
    It receives size of population, life span, number of children, density of population.
    Based on density and size of population it initiates a territory,
    where population lives.
    """

    def __init__(self, size, life_span=50, number_of_children=2, density=0.4):
        self.size = size
        self.life_span = life_span
        self.number_of_children = number_of_children
        self.density = density
        self.animals = []
        # Territory
        number_of_cells = int(size / density)
        dimensions = greatest_pair_of_factors(number_of_cells)
        self.territory = Territory(dimensions[0], dimensions[1])

    def generate(self):
        """
        Generate population
        """
        self.animals = [Animal(self.territory) for i in xrange(self.size)]
        self.territory.populate(self.animals, self.density)

    def show(self):
        # for row in self.territory.map:
        #     print(row)
        self.visualisation = visualize.PopulationVisualizer(self)
        self.visualisation.show()

    def get_map(self):
        """
        Return map of the territory
        """
        return self.territory.map

    def simulate_one_unit_of_time(self, speed):
        [animal.move(speed) for animal in self.animals]


def run_simulation(times=100, size=20, density=1):
    population = Population(200, density=1)
    population.generate()
    population.show()


if __name__ == '__main__':
    run_simulation()