#!/usr/bin/python3 -u

from collections import defaultdict
import math
import re


class Bot:
    def __init__(self):
        self.chips = []
        self.lo_pass = None
        self.hi_pass = None

    def __repr__(self):
        return f'Bot({self.chips=} {self.lo_pass=} {self.hi_pass=})'


bots = defaultdict(Bot)
outputs = defaultdict(list)


def load_instructions(instructions):
    spec1 = r'value (\d+) goes to bot (\d+)'
    spec2 = (r'bot (\d+) gives low to (bot|output) (\d+) '
             r'and high to (bot|output) (\d+)')

    for inst in instructions:
        if mo := re.fullmatch(spec1, inst):
            val = int(mo.group(1))
            bn = int(mo.group(2))
            bots[bn].chips.append(val)
            assert len(bots[bn].chips) < 3
        elif mo := re.fullmatch(spec2, inst):
            bn = int(mo.group(1))

            lo_type = mo.group(2)
            lo_id = int(mo.group(3))
            if lo_type == 'bot':
                bots[bn].lo_pass = bots[lo_id]
            else:
                bots[bn].lo_pass = lo_id

            hi_type = mo.group(4)
            hi_id = int(mo.group(5))
            if hi_type == 'bot':
                bots[bn].hi_pass = bots[hi_id]
            else:
                bots[bn].hi_pass = hi_id
        else:
            raise ValueError(f'bad instruction: {inst}')


def process_bots(c1, c2):
    outputs.clear()
    done = False
    target_chips = {c1, c2}
    bot_num = None
    while not done:
        done = True
        for bn, b in bots.items():
            if len(b.chips) == 2:
                if set(b.chips) == target_chips:
                    bot_num = bn  # this is the bot that did the comparison
                done = False
                lo_chip = min(b.chips)
                hi_chip = max(b.chips)
                assert b.lo_pass is not None and b.hi_pass is not None
                b.chips = []

                if isinstance(b.lo_pass, int):
                    outputs[b.lo_pass].append(lo_chip)
                else:
                    b.lo_pass.chips.append(lo_chip)

                if isinstance(b.hi_pass, int):
                    outputs[b.hi_pass].append(hi_chip)
                else:
                    b.hi_pass.chips.append(hi_chip)

    return bot_num


def part1(instructions):
    load_instructions(instructions)
    bot_num = process_bots(61, 17)
    return bot_num


def part2(instructions):
    part1(instructions)  # run this to populate outputs global
    return math.prod([outputs[n][0] for n in [0, 1, 2]])


def slurp(fname):
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2(inp))
        print()


if __name__ == '__main__':
    main()
