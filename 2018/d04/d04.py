#!/usr/bin/python3 -u

import re


def part1(logfile: list) -> int:
    guard = {}
    gid = None
    awake = True
    minute = 0

    # [1518-04-25 00:00] Guard #2381 begins shift
    gpat = re.compile(
        r'\[\d{4}-\d{2}-\d{2} \d{2}:(\d{2})] Guard #(\d+) begins shift')
    # [1518-04-23 00:46] falls asleep
    fpat = re.compile(r'\[\d{4}-\d{2}-\d{2} \d{2}:(\d{2})] falls asleep')
    # [1518-04-22 00:54] wakes up
    wpat = re.compile(r'\[\d{4}-\d{2}-\d{2} \d{2}:(\d{2})] wakes up')

    for line in logfile:
        # Note: the shift can start before midnight, but the problem only calls
        # for tracking awake/asleep times during the midnight hour, so we're
        # ignoring any minutes before midnight. The problem statement says,
        # "all asleep/awake times are during the midnight hour (00:00 - 00:59)".

        # guard log line
        if mo := re.fullmatch(gpat, line):
            # first, handle the previous guard's state
            if gid and not awake:
                for m in range(minute, 60):
                    guard[gid][m] += 1
            # second, start the new shift
            gid = int(mo.group(2))
            if gid not in guard:
                guard[gid] = [0] * 60  # this tracks sleep minutes
                minute = 0
                awake = True  # assume guards is awake when shift starts

        # 'falls asleep' log line
        elif mo := re.fullmatch(fpat, line):
            assert awake  # algorithm breaks otherwise
            minute = int(mo.group(1))
            awake = False

        # 'wakes up' log line
        elif mo := re.fullmatch(wpat, line):
            assert not awake  # algorithm breaks otherwise
            new_minute = int(mo.group(1))
            for m in range(minute, new_minute):
                guard[gid][m] += 1
            minute = new_minute
            awake = True

        else:
            raise ValueError(f'bad input: {line}')

    most_sleepy_gid = None
    max_sleep_time = -1
    for gid in guard:
        sleep_time = sum(guard[gid])
        if sleep_time > max_sleep_time:
            max_sleep_time = sleep_time
            most_sleepy_gid = gid

    most_sleepy_minute = (
        guard[most_sleepy_gid].index(max(guard[most_sleepy_gid])))

    return most_sleepy_gid * most_sleepy_minute


def part2():
    return None


def slurp(fname: str) -> list[str]:
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def main():
    sample_input = sorted(slurp('input/sample_input.txt'))
    main_input = sorted(slurp('input/input.txt'))

    for inp in (sample_input, main_input):
        print("Part 1 answer =", part1(inp))
        print("Part 2 answer =", part2())
        print()


if __name__ == '__main__':
    main()
