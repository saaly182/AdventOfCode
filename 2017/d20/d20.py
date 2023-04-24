#!/usr/bin/python3 -u

import dataclasses
import re


@dataclasses.dataclass
class Particle:
    n: int
    p: tuple
    v: tuple
    a: tuple


def part1_sortkey(part):
    a2 = sum([a_component**2 for a_component in part.a])
    v2 = sum([v_component**2 for v_component in part.v])
    p2 = sum([p_component**2 for p_component in part.p])
    return a2, v2, p2


def part1(initial_particles: tuple) -> int:
    """
    'the GPU would like to know which particle will stay closest to position
    <0,0,0> in the long term'. As t->infinity, acceleration will dominate dist
    from origin. So the particle with the lowest acceleration will be closest.
    If there is a tie for lowest accel., then rank by lowest initial velocity,
    then by closest initial position.
    """
    particles = sorted(initial_particles, key=part1_sortkey)
    return particles[0].n


def part2():
    return None


def slurp(fname: str) -> list[str]:
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def parse(inp: list) -> tuple:
    # example input line: p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>
    particles = []
    pdata = re.compile(r'p=<(-?\d+),(-?\d+),(-?\d+)>, '
                       r'v=<(-?\d+),(-?\d+),(-?\d+)>, '
                       r'a=<(-?\d+),(-?\d+),(-?\d+)>')
    for n, line in enumerate(inp):
        mo = re.match(pdata, line)
        if not mo:
            raise ValueError(f'bad input line: {line}')
        part = Particle(n=n,
                        p=(int(mo[1]), int(mo[2]), int(mo[3])),
                        v=(int(mo[4]), int(mo[5]), int(mo[6])),
                        a=(int(mo[7]), int(mo[8]), int(mo[9])))
        particles.append(part)

    return tuple(particles)


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        initial_particles = parse(inp)
        print("Part 1 answer =", part1(initial_particles))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
