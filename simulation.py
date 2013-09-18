import random
import visualize
import support


LENGTH_OF_INTERACTION = 5
LENGTH_OF_REST = 10
DISTANCE_OF_INTERACTION = 0.1
PROBABILITY_OF_MUTATION = 0.2


class Territory(object):
    """
    Represents a territory, where animals live.
    Initializes with an empty map
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.agents = []

    def is_point_inside(self, coord):
        return 0 < coord[0] < self.width and 0 < coord[1] < self.height

    def occupy_cell(self, x, y, agent):
        """
        Records (x, y) for animal
        """
        y = int(round(y) - 0.5)
        agent.x = x + random.random()
        agent.y = y + random.random()
        self.agents.append(agent)

    def populate(self, agents, density):
        """
        Populates the territory with agents with population density.
        It calculates the square, in which one agent lives.
        """
        self.agents = []
        agents = agents[:]
        for_one_agent = 1.0 / density
        x = 0
        while x < self.width:
            y = for_one_agent
            while y <= self.height:
                self.occupy_cell(x, y, agents.pop())
                y += for_one_agent
            x += 1

    def agent_for_interaction(self, agent):
        """
        Returns agent, that is close enough and the closest to begin interaction
        """
        closest_distance = DISTANCE_OF_INTERACTION
        closest = None
        for another_agent in self.agents:
            if another_agent == agent:
                continue
            dist = support.distance((agent.x, agent.y), (another_agent.x, another_agent.y))
            if dist < closest_distance:
                closest = another_agent
                closest_distance = dist
        return closest

    def update(self, agents):
        self.agents = agents

class Animal(object):
    """
    Represents an animal.
    Basic class for different behaviours
    """

    def __init__(self, population, territory, strategy=0):
        self.territory = territory
        self.population = population
        self.x = 0
        self.y = 0
        self.strategy = strategy
        self.interacting_with = None
        self.interaction_time_left = 0
        self.unavailable_for = 0
        self.moved = False
        self.score = 0

    def live_one_unit_of_time(self, speed):
        """
        Moves if can, interacts if can
        """
        # Can be already moved if some animal has started interaction with this animal
        if self.moved:
            return

        self.moved = True

        # Unavailable for some time after interaction
        if self.unavailable_for > 0:
            self.unavailable_for -= 1
            self.move(speed)
            return

        if self.interacting_with is not None:
            # If still in interaction
            if self.interaction_time_left > 0:
                self.interaction_time_left -= 1
                return
            else:
                self.stop_interaction()

        if speed > self.territory.width and speed > self.territory.height:
            return

        self.move(speed)
        self.interact_with(self.territory.agent_for_interaction(self))

    def move(self, speed):
        # Find new place
        new_coord = support.calculate_new_point_in_random_direction((self.x, self.y), speed)
        while not self.territory.is_point_inside(new_coord):
            new_coord = support.calculate_new_point_in_random_direction((self.x, self.y), speed)
        self.x, self.y = new_coord

    def interact_with(self, animal):
        if animal is not None and animal.able_to_interact() and self.able_to_interact():
            self.interaction_time_left = LENGTH_OF_INTERACTION
            animal.interaction_time_left = LENGTH_OF_INTERACTION
            animal.interacting_with = self
            animal.moved = True
            self.interacting_with = animal
            outcome = self.population.game.outcome(self.strategy, animal.strategy)
            self.score += outcome[0]
            animal.score += outcome[1]

    def stop_interaction(self):
        animal = self.interacting_with
        animal.interacting_with = None
        animal.unavailable_for = LENGTH_OF_REST
        self.interacting_with = None
        self.unavailable_for = LENGTH_OF_REST

    def able_to_interact(self):
        return self.unavailable_for == 0 and self.interacting_with is None

    def reproduce(self, number_of_children):
        children = []
        for i in xrange(number_of_children):
            mutation_takes_place = random.random() < PROBABILITY_OF_MUTATION
            if mutation_takes_place:
                child_strategy = 1 - self.strategy
            else:
                child_strategy = self.strategy
            child = Animal(self.population, self.territory, child_strategy)
            child.x = self.x + random.random()*0.2
            child.y = self.y + random.random()*0.2
            children.append(child)
        return children


class Population(object):
    """
    Represents a population, consisted of animals (Animal class).
    It receives size of population, life span, number of children, density of population.
    Based on density and size of population it initiates a territory,
    where population lives.
    """

    def __init__(self, game, size, life_span, density):
        self.game = game
        self.size = size
        self.life_span = life_span
        self.density = density
        self.years_to_live = life_span
        self.animals = []
        # Territory
        number_of_cells = int(size / density)
        dimensions = support.greatest_pair_of_factors(number_of_cells)
        self.territory = Territory(dimensions[0], dimensions[1])

    def generate(self):
        """
        Generate population
        """
        self.animals = [Animal(self, self.territory) for i in xrange(self.size)]

        number_of_strategy0 = int(self.size*self.game.percentages[0])
        number_of_strategy1 = self.size - number_of_strategy0
        strategies = [0 for i in xrange(number_of_strategy0)]
        strategies += [1 for i in xrange(number_of_strategy1)]
        random.shuffle(strategies)
        for i in xrange(self.size):
            self.animals[i].strategy = strategies[i]

        self.territory.populate(self.animals, self.density)
        # So animals won't be sorted by coordinates
        random.shuffle(self.animals)

    def show(self):
        # for row in self.territory.map:
        #     print(row)
        self.visualisation = visualize.PopulationVisualizer()
        self.visualisation.show()

    def simulate_one_unit_of_time(self, speed):
        [animal.live_one_unit_of_time(speed) for animal in self.animals]
        for animal in self.animals:
            animal.moved = False
        self.years_to_live -= 1
        if self.years_to_live == 0:
            self.reproduce()

    def reproduce(self):
        sorted_by_score = sorted(self.animals, key=lambda x: x.score, reverse=True)
        new_generation = []
        for i in xrange(int(self.size*0.25)):
            new_generation += sorted_by_score[i].reproduce(number_of_children=2)
        for i in xrange(int(self.size*0.25), int(self.size*0.75)):
            new_generation += sorted_by_score[i].reproduce(number_of_children=1)
        self.animals = new_generation
        random.shuffle(self.animals)
        self.territory.update(self.animals)
        self.years_to_live = self.life_span


class Strategy(object):
    """
    Represent line of the behaviour for agents
    identifier (string) - name of the strategy
    """
    def __init__(self, identifier):
        self.identifier = identifier


class Hawk(Strategy):
    """
    Hawk behaviour
    """
    def __int__(self):
        super(Hawk, self).__init__("Hawk")


class Pigeon(Strategy):
    """
    Pigeon behaviour
    """
    def __int__(self):
        super(Pigeon, self).__init__("Pigeon")


class Game(object):
    """
    Represents the table of outcomes:
    __________| Strategy0 | Strategy1
    Strategy0 |    5, 10  |   -5, -5
    Strategy1 |   -5, -5  |   0, 0
    For this table, parameters should be:
    strategies = [strategy0_identifier, strategy1_identifier]
    outcomes = [[(5, 10), (-5, -5)], [(-5, -5), (0, 0)]]

    percentages - percentage of population, following this strategy
    """
    def __init__(self, outcomes, percentages=(0.5, 0.5)):
        self.outcomes = outcomes
        self.percentages = percentages

    def outcome(self, strategy0, strategy1):
        return self.outcomes[strategy0][strategy1]


# def run_simulation(game, times=100, size=20, density=1):
#     population = Population(game, 100, density=1)
#     population.generate()
#     population.show()
#
#
if __name__ == '__main__':
    # _______|     Hawk   | Pigeon
    # Hawk   |  -40, -40  |  -30, 50
    # Pigeon |   50, -30  |  -5, -5
    # game = Game([[(-8, -8), (-6, 10)], [(10, -6), (-1, -1)]])
    # run_simulation(game, times=10)
    visualizer = visualize.PopulationVisualizer()
    visualizer.show()