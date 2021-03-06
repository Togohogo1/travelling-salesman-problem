from numpy import exp  # Avoid overflow
from random import sample, random
import plotter


def calc_dist(dist_from, cities):
    return sum(dist_from[c1][c2] for c1, c2 in zip(cities[1:], cities[:-1]))


def evaluate(dist_from, best_tour, x_coord, y_coord, temp, solution):
    title = f"Temperature: {temp:.2f}, Distance: {calc_dist(dist_from, best_tour):.2f}"
    plotter.plot_path(x_coord, y_coord, best_tour, title, solution)
    plotter.draw_path()


# Section of path replaced with same cities running in opposite order
def neighbour(best_tour, city_count):
    next_tour = best_tour[:]
    l, r = sorted(sample(range(1, city_count+1), 2))
    next_tour[l:r] = next_tour[l:r][::-1]
    return next_tour


# Acceptance probability function via Metropolis-Hastings algorithm
def metropolis(dist_from, old, new, temp):
    dist_old = calc_dist(dist_from, old)
    dist_new = calc_dist(dist_from, new)

    # if `dist_old - dist_new` >= 0, new tour better than old tour
    # Otherwise, the greater the temp, the more likely it is to switch to a worse tour (to potentially reach a better local min)
    if random() < exp((dist_old-dist_new)/temp):
        old[:] = new


# Source: https://www.cec.uchile.cl/cinetica/pcordero/MC_libros/NumericalRecipesinC.pdf, p. 444
def run(x_coord, y_coord, dist_from, city_count, solution=None):
    temperature = 100
    r = 0.99999
    ε = 0.001
    best_tour = [0] + sample(range(1, city_count), city_count-1) + [0]

    while temperature > 1:
        temperature *= r  # Geom sequence, T0(r)^x
        next_tour = neighbour(best_tour, city_count)

        # If exact temperature close to rounded temperature (less than an absolute difference of `temperature - ε`)
        # Smaller `ε` results in less evaluations
        if abs(temperature-ε) <= int(temperature):
            evaluate(dist_from, best_tour, x_coord, y_coord, temperature, solution)

        metropolis(dist_from, best_tour, next_tour, temperature)

    return best_tour
