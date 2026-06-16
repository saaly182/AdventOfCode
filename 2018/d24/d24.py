#!/usr/bin/python3 -u

import re


class Group:
    def __init__(self, group_descriptor: tuple):
        assert len(group_descriptor) == 9
        self.group_id = None
        self.unit_count = int(group_descriptor[0])
        self.hitpoints = int(group_descriptor[1])
        self.attack_damage = int(group_descriptor[6])
        self.attack_type = group_descriptor[7]
        self.initiative = int(group_descriptor[8])
        self.weaknesses = ()
        self.immunities = ()
        self.target = None

        # parse weaknesses and immunities
        for i in (2, 4):
            if group_descriptor[i] == 'weak':
                self.weaknesses = tuple(group_descriptor[i + 1].split(', '))
            elif group_descriptor[i] == 'immune':
                self.immunities = tuple(group_descriptor[i + 1].split(', '))
        assert set(self.weaknesses).intersection(set(self.immunities)) == set()

    def __str__(self):
        return (f'id={self.group_id} units={self.unit_count} '
                f'hitpoints={self.hitpoints} '
                f'attack_damage={self.attack_damage} '
                f'attack_type={self.attack_type} initiative={self.initiative} '
                f'weaknesses={self.weaknesses} '
                f'immunities={self.immunities}')

    def effective_power(self) -> int:
        return self.unit_count * self.attack_damage

    def inflicted_damage(self, eg: Group) -> int:
        """Return the damage that would be inflicted on the enemy group."""
        d = self.effective_power()
        if self.attack_type in eg.immunities:
            d = 0
        if self.attack_type in eg.weaknesses:
            d *= 2
        return d


class Army:
    def __init__(self, name: str):
        self.name = name
        self.groups = []
        self.enemy = None

    def size(self):
        return sum([g.unit_count for g in self.groups])

    def add_group(self, g: Group) -> None:
        self.groups.append(g)
        g.group_id = len(self.groups)

    def show(self):
        print(f'Army: {self.name}')
        for g in self.groups:
            print('    ', g)

    @staticmethod
    def __by_ep_and_init(g: Group):
        return g.effective_power(), g.initiative

    def select_targets(self):
        """
        During the target selection phase, each group attempts to choose one
        target. In decreasing order of effective power, groups choose their
        targets; in a tie, the group with the higher initiative chooses
        first. The attacking group chooses to target the group in the enemy
        army to which it would deal the most damage (after accounting for
        weaknesses and immunities, but not accounting for whether the
        defending group has enough units to actually receive all of that
        damage).

        If an attacking group is considering two defending groups to which it
        would deal equal damage, it chooses to target the defending group
        with the largest effective power; if there is still a tie, it chooses
        the defending group with the highest initiative. If it cannot deal
        any defending groups damage, it does not choose a target. Defending
        groups can only be chosen as a target by one attacking group.

        At the end of the target selection phase, each group has selected
        zero or one groups to attack, and each group is being attacked by
        zero or one groups.
        """
        # reset any old targets
        for g in self.groups:
            g.target = None

        available_targets = [eg for eg in self.enemy.groups
                             if eg.unit_count > 0]

        for g in sorted(self.groups, key=self.__by_ep_and_init, reverse=True):
            maxi = maxd = maxep = maxinit = -1
            for i, eg in enumerate(available_targets):
                d = g.inflicted_damage(eg)
                ep = eg.effective_power()
                init = eg.initiative
                if (d, ep, init) > (maxd, maxep, maxinit):
                    maxi = i
                    maxd = d
                    maxep = ep
                    maxinit = init
            if maxi >= 0:
                g.target = available_targets[maxi]
                del available_targets[maxi]


def battle(inf: Army, imm: Army):
    """
    During the attacking phase, each group deals damage to the target it
    selected, if any. Groups attack in decreasing order of initiative,
    regardless of whether they are part of the infection or the immune
    system. (If a group contains no units, it cannot attack.)
    """
    for g in sorted(inf.groups + imm.groups,
                    key=(lambda gr: gr.initiative), reverse=True):
        attacker = g
        defender = g.target

        if attacker.unit_count == 0 or defender is None:
            continue

        killed_units = attacker.inflicted_damage(defender) // defender.hitpoints
        defender.unit_count = max(defender.unit_count - killed_units, 0)


def part1(inf: Army, imm: Army) -> int:
    while inf.size() > 0 and imm.size() > 0:
        inf.select_targets()
        imm.select_targets()
        battle(inf, imm)

    return inf.size() + imm.size()


def part2() -> int:
    return -99


def parse_input(fname: str) -> tuple[Army, Army]:
    inf = Army('Infection')
    imm = Army('Immune System')

    inf.enemy = imm
    imm.enemy = inf

    # example:
    # 585 units each with 5936 hit points (weak to cold; immune to fire) with
    # an attack that does 17 slashing damage at initiative 17
    group_pattern = (
        r'(\d+) units each with (\d+) hit points '
        r'(?:\((weak|immune) to ([a-z, ]+)'
        r'(?:; (weak|immune) to ([a-z, ]+))?\) )?'
        r'with an attack that does (\d+) ([a-z]+) damage at initiative (\d+)'
    )
    group_re = re.compile(group_pattern)

    curr_army = None
    with open(fname) as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            elif line == 'Infection:':
                curr_army = inf
            elif line == 'Immune System:':
                curr_army = imm
            elif mo := group_re.fullmatch(line):
                assert curr_army
                curr_army.add_group(Group(mo.groups()))
            else:
                raise ValueError(f'Invalid input: "{line}"')

    return inf, imm


def main():
    sample_input = parse_input('input/sample_input.txt')
    main_input = parse_input('input/input.txt')

    for inf, imm in (sample_input, main_input):
        print("Part 1 answer =", part1(inf, imm))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
