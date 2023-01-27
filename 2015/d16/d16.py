#!/usr/bin/python3 -u

real_aunt_sue = {
    ('children', 3),
    ('cats', 7),
    ('samoyeds', 2),
    ('pomeranians', 3),
    ('akitas', 0),
    ('vizslas', 0),
    ('goldfish', 5),
    ('trees', 3),
    ('cars', 2),
    ('perfumes', 1),
}


def part1(aunts):
    for aunt_num in aunts:
        if aunts[aunt_num].issubset(real_aunt_sue):
            return aunt_num
    return None


def part2(aunts):
    """
    In particular, the cats and trees readings indicates that there are
    greater than that many (due to the unpredictable nuclear decay of cat
    dander and tree pollen), while the pomeranians and goldfish readings
    indicate that there are fewer than that many (due to the modial
    interaction of magnetoreluctance).
    """
    rasd = {k: v for (k, v) in real_aunt_sue}
    for aunt_num, things in aunts.items():
        found_aunt = True
        for thing, count in things:
            if thing not in rasd:
                found_aunt = False
            match thing:
                case ('cats' | 'trees') as gt_thing:
                    if count <= rasd[gt_thing]:
                        found_aunt = False
                case ('pomeranians' | 'goldfish') as lt_thing:
                    if count >= rasd[lt_thing]:
                        found_aunt = False
                case _ as eq_thing:
                    if count != rasd[eq_thing]:
                        found_aunt = False
            if not found_aunt:
                break
        if found_aunt:
            return aunt_num
    return None


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def parse(inp):
    aunts = {}
    for line in inp:
        a = line.replace(':', '').replace(',', '').split()
        aunt_num = int(a[1])
        aunts[aunt_num] = set()
        for thing, count in zip(a[2::2], a[3::2]):
            aunts[aunt_num].add((thing, int(count)))
    return aunts


def main():
    main_input = slurp('input/input.txt')

    for inp in (main_input, ):
        aunts = parse(inp)
        print("Part 1 answer =", part1(aunts))
        print("Part 2 answer =", part2(aunts))
        print()


if __name__ == '__main__':
    main()
