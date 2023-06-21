#!/usr/bin/python3 -u

import collections


class Node:
    def __init__(self, nums: list):
        # recursively creates child Nodes, and also consumes the nums list
        self.id = len(nums)
        self.num_children = nums.pop()
        self.num_metadata = nums.pop()
        self.children = []
        self.metadata = []
        for c in range(self.num_children):
            self.children.append(Node(nums))
        for m in range(self.num_metadata):
            self.metadata.append(nums.pop())

    def value(self):
        if not self.children:
            val = sum(self.metadata)
        else:
            val = 0
            for m in self.metadata:
                if m < 1 or m > self.num_children:
                    continue
                val += self.children[m - 1].value()
        return val

    def __repr__(self):
        return f'Node({self.id=} {self.children=} {self.metadata=})'


def part1(input_nums: tuple) -> int:
    root = Node(list(reversed(input_nums)))
    metadata_sum = 0
    q = collections.deque([root])
    while q:
        node = q.popleft()
        metadata_sum += sum(node.metadata)
        q.extend(node.children)

    return metadata_sum


def part2(input_nums: tuple) -> int:
    root = Node(list(reversed(input_nums)))
    return root.value()


def slurp(fname: str) -> list[str]:
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (sample_input, main_input):
        input_nums = tuple([int(x) for x in inp[0].split()])
        print("Part 1 answer =", part1(input_nums))
        print("Part 2 answer =", part2(input_nums))
        print()


if __name__ == '__main__':
    main()
