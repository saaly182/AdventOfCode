#!/usr/bin/python3 -u

import re


EMPTY_BLOCK = -1


def consolidate_freespace(disk: list) -> None:
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


def index_free_slots(disk: tuple, f_start: int, f_size: int) -> tuple:
    """Index empty slots before f_start and at least f_size"""
    idx = []
    diskstr = ''.join(['.' if x == EMPTY_BLOCK else 'F' for x in disk])
    pat = r'\.' * f_size + r'+'
    for mo in re.finditer(pat, diskstr):
        if mo.start() < f_start:
            e_start = mo.start()
            e_size = mo.end() - mo.start()
            idx.append((e_start, e_size))
        else:
            break
    return tuple(idx)


def fileinfo(disk: tuple, file_num: int) -> tuple[int, int]:
    diskstr = ''.join(['F' if x == file_num else '*' for x in disk])
    mo = re.search(r'F+', diskstr)
    assert mo
    return mo.start(), mo.end() - mo.start()


def part1(disk: list) -> int:
    consolidate_freespace(disk)
    return fs_checksum(disk)


def part2(disk: list) -> int:
    for file_num in range(max(disk), 0, -1):
        f_start, f_size = fileinfo(tuple(disk), file_num)
        free_slots = index_free_slots(tuple(disk), f_start, f_size)
        for e_start, e_size in free_slots:
            if e_size >= f_size and e_start < f_start:
                # move file
                disk[e_start:e_start + f_size] = [file_num] * f_size
                # set file's original location to 'empty'
                disk[f_start:f_start + f_size] = [EMPTY_BLOCK] * f_size
                break
    return fs_checksum(disk)


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
        print("Part 1 answer =", part1(inp[:]))
        print("Part 2 answer =", part2(inp[:]))
        print()


if __name__ == '__main__':
    main()
