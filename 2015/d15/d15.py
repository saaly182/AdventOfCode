#!/usr/bin/python3 -u

import itertools
import math


def cookie_score(ingredients, teaspoons):
    propvals = []
    for p in range(4):
        propval = sum([ingredients[ing][p] * tsp for ing, tsp in
                       zip(ingredients, teaspoons)])
        if propval < 0:
            propval = 0
        propvals.append(propval)
    return math.prod(propvals)


def cookie_calories(ingredients, teaspoons):
    return sum([ingredients[ing][4] * tsp for ing, tsp in
                zip(ingredients, teaspoons)])


def part1(ingredients, fixed_calories=None):
    num_ing = len(ingredients)
    best_score = 0

    for teaspoons in itertools.product(range(101), repeat=num_ing):
        if sum(teaspoons) != 100:
            continue
        if fixed_calories is None:
            best_score = max(best_score, cookie_score(ingredients, teaspoons))
        else:
            if cookie_calories(ingredients, teaspoons) == fixed_calories:
                best_score = max(best_score,
                                 cookie_score(ingredients, teaspoons))

    return best_score


def part2(ingredients):
    return part1(ingredients, fixed_calories=500)


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def parse(inp):
    ingredients = {}
    for line in inp:
        a = line.replace(':', '').replace(',', '').split()
        ingredients[a[0]] = tuple(int(x) for x in a[2::2])
    return ingredients


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        ingredients = parse(inp)
        print("Part 1 answer =", part1(ingredients))
        print("Part 2 answer =", part2(ingredients))
        print()


if __name__ == '__main__':
    main()
