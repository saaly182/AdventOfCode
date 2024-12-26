#!/usr/bin/python3 -u


def blink(stones: list) -> list:
    st = []
    for stone in stones:
        sstr = str(stone)
        sl = len(sstr)
        if stone == 0:
            st.append(1)
        elif sl % 2 == 0:
            mid_idx = sl // 2
            sleft = int(sstr[:mid_idx])
            sright = int(sstr[mid_idx:])
            st.append(sleft)
            st.append(sright)
        else:
            st.append(stone * 2024)
    return st


def part1(stones: list, blink_count: int) -> int:
    for i in range(blink_count):
        stones = blink(stones)
    return len(stones)


def part2(stones: list, blink_count: int) -> int:
    return part1(stones, blink_count)


def slurp(fname: str) -> tuple[str, ...]:
    with open(fname) as file:
        return tuple(line.rstrip() for line in file.readlines())


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        stones = [int(x) for x in inp[0].split()]
        print("Part 1 answer =", part1(stones[:], 25))
        print("Part 2 answer =", part2(stones[:], 75))
        print()


if __name__ == '__main__':
    main()
