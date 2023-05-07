#!/usr/bin/python3 -u

# https://www.reddit.com/r/adventofcode/comments/7kz6ik/comment/drik99m/?utm_source=reddit&utm_medium=web2x&context=3

import collections
import copy
import dataclasses
import itertools
import re


@dataclasses.dataclass
class Particle:
    n: int    # id
    p: tuple  # position
    v: tuple  # velocity
    a: tuple  # acceleration


def part1_sortkey(part):
    a2 = sum([a_component**2 for a_component in part.a])
    v2 = sum([v_component**2 for v_component in part.v])
    p2 = sum([p_component**2 for p_component in part.p])
    return a2, v2, p2


def part1(initial_particles: tuple) -> int:
    # 'the GPU would like to know which particle will stay closest to position
    # <0,0,0> in the long term'. As t->infinity, acceleration will dominate dist
    # from origin. So the particle with the lowest acceleration will be closest.
    # If there is a tie for lowest accel., then rank by lowest initial velocity,
    # then by closest initial position.
    # Update: this logic is not completely correct. Absolute acceleration is
    # right but for equal acceleration, absolute velocity is not correct.
    # Consider:
    #     p=<0,0,0>, v=<0,0,0>, a=<1,0,0>
    #     p=<0,0,0>, v=<-1,0,0>, a=<1,0,0>
    # TODO: fix the velocity logic problem
    particles = sorted(initial_particles, key=part1_sortkey)
    return particles[0].n


def dot_product(a: tuple, b: tuple) -> int:
    return sum(x * y for x, y in zip(a, b, strict=True))


def approaching_vertex(p: Particle) -> bool:
    # A particle is still approaching its vertex if the component of velocity
    # in the acceleration direction is in the opposite direction as the
    # acceleration. That is true if the dot product of velocity and
    # acceleration is < 0. This also works for the zero acceleration (straight
    # line) case, because the dot product will be zero.
    return dot_product(p.v, p.a) < 0


def remove_collisions(particles: list[Particle]) -> None:
    positions = collections.defaultdict(list)
    for particle in particles:
        positions[particle.p].append(particle)
    for position, partlist in positions.items():
        if len(partlist) > 1:
            for part in partlist:
                particles.remove(part)


def vector_add(a: tuple, b: tuple) -> tuple:
    vsum = []
    for ai, bi in zip(a, b, strict=True):
        vsum.append(ai + bi)
    return tuple(vsum)


def time_step(particles: list[Particle]) -> None:
    for particle in particles:
        particle.v = vector_add(particle.v, particle.a)
        particle.p = vector_add(particle.p, particle.v)


def all_diverging(particles: list[Particle]) -> bool:
    for part_a, part_b in itertools.combinations(particles, 2):
        pa = copy.copy(part_a)
        pb = copy.copy(part_b)
        mandist1 = sum(abs(x - y) for x, y in zip(pa.p, pb.p))
        time_step([pa, pb])
        mandist2 = sum(abs(x - y) for x, y in zip(pa.p, pb.p))
        if mandist2 < mandist1 or mandist1 == 0:
            return False
    return True


def part2(initial_particles: tuple) -> int:
    # 'How many particles are left after all collisions are resolved?'
    # I know this can be solved by figuring out all the parameterized quadratics
    # and determining time points where collisions occur. That approach
    # eliminates the challenge of figuring out when to stop the computations,
    # but I don't feel like working out all the math details.
    #
    # So instead I'm just going to run the simulation and catch collisions at
    # each time step. The stopping condition is: there will be no more
    # collisions after all the particles are past their parabola's vertex
    # *and* each pair of particles is moving away from each other. I'll use
    # the vector dot product to determine when a particle has passed its vertex.

    particles = list(initial_particles)
    while True:
        remove_collisions(particles)
        time_step(particles)
        if any([approaching_vertex(p) for p in particles]):
            continue
        if all_diverging(particles):
            break

    return len(particles)


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
        print("Part 2 answer =", part2(initial_particles))
        print()


if __name__ == '__main__':
    main()
