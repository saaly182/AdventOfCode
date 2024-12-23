#!/usr/bin/python3 -u

EMPTY_BLOCK = -1


def defrag(disk: list) -> None:
    last_used = 0
    while True:
        first_empty = disk.index(EMPTY_BLOCK)
        # brute force...
        for i, x in enumerate(reversed(disk)):
            if x != EMPTY_BLOCK:
                last_used = len(disk) - i - 1
                break
        if first_empty < last_used:
            disk[first_empty] = disk[last_used]
            disk[last_used] = EMPTY_BLOCK
        else:
            break


def fs_checksum(disk: list) -> int:
    csum = 0
    for i, x in enumerate(disk):
        if x == EMPTY_BLOCK:
            continue
        csum += (x * i)
    return csum


def show(disk: list) -> None:
    d = ['.' if x == EMPTY_BLOCK else str(x) for x in disk]
    print(''.join(d))


def part1(disk: list) -> int:
    defrag(disk)
    return fs_checksum(disk)


def part2():
    return None


def slurp(fname: str) -> list[int]:
    disk = []
    with open(fname) as file:
        diskmap = file.readline().rstrip()

    is_freespace = False
    file_num = 0
    for x in diskmap:
        blockcount = int(x)
        if is_freespace:
            disk.extend([EMPTY_BLOCK] * blockcount)
        else:
            disk.extend([file_num] * blockcount)
            file_num += 1
        is_freespace = not is_freespace

    return disk


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
