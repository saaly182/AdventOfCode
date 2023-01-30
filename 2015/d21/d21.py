#!/usr/bin/python3 -u

from dataclasses import dataclass


@dataclass
class Equipment:
    name: str
    cost: int
    damage: int
    armor: int


@dataclass
class Character:
    hitpoints: int = 0
    damage: int = 0
    armor: int = 0


shop = {
    'weapons': (
        Equipment('Dagger', 8, 4, 0),
        Equipment('Shortsword', 10, 5, 0),
        Equipment('Warhammer', 25, 6, 0),
        Equipment('Longsword', 40, 7, 0),
        Equipment('Greataxe', 74, 8, 0),
    ),
    'armor': (
        Equipment('Leather', 13, 0, 1),
        Equipment('Chainmail', 31, 0, 2),
        Equipment('Splintmail', 53, 0, 3),
        Equipment('Bandedmail', 75, 0, 4),
        Equipment('Platemail', 102, 0, 5),
    ),
    'rings': (
        Equipment('Damage +1', 25, 1, 0),
        Equipment('Damage +2', 50, 2, 0),
        Equipment('Damage +3', 100, 3, 0),
        Equipment('Defense +1', 20, 0, 1),
        Equipment('Defense +2', 40, 0, 2),
        Equipment('Defense +3', 80, 0, 3),
    )
}


def death_hit(hitpoints, attack_loss):
    """Return the hit number where hitpoints becomes <= 0."""
    dh = hitpoints // attack_loss
    if hitpoints % attack_loss == 0:
        dh -= 1
    return dh


def who_wins(p1, p2):
    p1_wins = 1
    p2_wins = 2

    p1_hp_decr = max(1, p2.damage - p1.armor)
    p2_hp_decr = max(1, p1.damage - p2.armor)
    p1_death_hit = death_hit(p1.hitpoints, p1_hp_decr)
    p2_death_hit = death_hit(p2.hitpoints, p2_hp_decr)
    if p1_death_hit >= p2_death_hit:
        return p1_wins
    else:
        return p2_wins


def part1(boss, objective='win'):
    player_hitpoints = 100
    empty_item = Equipment('nothing', 0, 0, 0)
    cost_min = float('inf')
    cost_max = float('-inf')

    for weapon in shop['weapons']:
        for armor in (empty_item,) + shop['armor']:
            for ring1 in (empty_item,) + shop['rings']:
                for ring2 in (empty_item,) + shop['rings']:
                    if ring2 == ring1:
                        continue
                    d = weapon.damage + ring1.damage + ring2.damage
                    a = armor.armor + ring1.armor + ring2.armor
                    cost = weapon.cost + armor.cost + ring1.cost + ring2.cost
                    player = Character(player_hitpoints, d, a)

                    # track optimal cost for player
                    if who_wins(player, boss) == 1:
                        if cost < cost_min:
                            cost_min = cost
                    # track optimal cost for shopkeeper+boss
                    else:
                        if cost > cost_max:
                            cost_max = cost

    return cost_min if objective == 'win' else cost_max


def part2(boss):
    return part1(boss, objective='lose')


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def main():
    boss = Character(104, 8, 1)
    print("Part 1 answer =", part1(boss))
    print("Part 2 answer =", part2(boss))
    print()


if __name__ == '__main__':
    main()
