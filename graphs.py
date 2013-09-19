import cProfile
import population
import matplotlib.pyplot as plt


def run_simulation(population, speed=0.2, times=100):
    population.generate()
    strategies_statistics = []
    for i in range(times*population.life_span):
        population.simulate_one_unit_of_time(speed)
        strategies_statistics.append(population.get_strategy_numbers())
    strategy1_numbers = [numbers[0] for numbers in strategies_statistics]
    strategy2_numbers = [numbers[1] for numbers in strategies_statistics]
    plt.plot(strategy1_numbers, label=population.get_strategy_name(0))
    plt.plot(strategy2_numbers, label=population.get_strategy_name(1))
    plt.title("Changes in number of agents following the strategy.")
    plt.xlabel("Time")
    plt.ylabel("Number of agents")
    plt.legend()
    plt.show()

game = population.Game([[[-8, -8], [-6, 10]], [[10, 06], [-1, -1]]], names=('Hawk', 'Pigeon'), percentages=(0.9, 0.1))
population = population.Population(game, 100, 20, 1)
cProfile.run('run_simulation(population, times=10)')