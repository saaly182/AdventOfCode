#!/usr/bin/python3 -u

class TransformRules:
    def __init__(self, rulelines: list) -> None:
        self._rules = self._parse(rulelines)

    def transform(self, pattern: str) -> str:
        return self._rules[pattern]

    def _parse(self, rulelines: list) -> dict:
        rules = {}
        for line in rulelines:
            in_pattern, out_pattern = line.split(' => ')
            for in_pat in self._all_variations(in_pattern):
                if in_pat in rules:
                    raise ValueError(f'Input already covers {in_pat}')
                rules[in_pat] = out_pattern
        return rules

    def _all_variations(self, pattern: str) -> tuple:
        """Return all unique rotations/flips of the pattern."""
        variations = set()
        grid = self.pattern_to_grid(pattern)
        for i in range(2):
            grid = self._grid_flip(grid)
            for j in range(4):
                grid = self._grid_rotate(grid)
                variations.add(self.grid_to_pattern(grid))
        return tuple(variations)

    @staticmethod
    def pattern_to_grid(pattern: str) -> list:
        return [list(row) for row in pattern.split('/')]

    @staticmethod
    def grid_to_pattern(grid: list) -> str:
        return '/'.join([''.join(row) for row in grid])

    @staticmethod
    def _grid_flip(grid: list) -> list:
        return list(reversed(grid))

    @staticmethod
    def _grid_rotate(grid: list) -> list:
        return list(zip(*reversed(grid)))


def showgrid(grid: list) -> None:
    print('-' * 50)
    for row in grid:
        print(' '.join(row))


def gen_pattern(grid: list, r0: int, c0: int, chunk_size: int) -> str:
    pattern = []
    for r in range(chunk_size):
        for c in range(chunk_size):
            pattern.append(grid[r + r0][c + c0])
        pattern.append('/')
    return ''.join(pattern[:-1])  # dropping final '/'


# tons of credit to
# https://www.reddit.com/r/adventofcode/comments/7l78eb/comment/drk5098/?utm_source=reddit&utm_medium=web2x&context=3 # noqa
def part1(rules: TransformRules, iterations: int) -> int:
    grid = [['.', '#', '.'],
            ['.', '.', '#'],
            ['#', '#', '#']]

    # throughout, a '2' suffix on a variable refers to the next grid
    for iteration in range(iterations):
        current_size = len(grid)
        if current_size % 2 == 0:
            chunk_size = 2
            size2 = current_size // 2 * 3
        else:
            chunk_size = 3
            size2 = current_size // 3 * 4

        grid2 = [[] for _ in range(size2)]
        chunk2 = None
        r2 = 0
        for r in range(0, current_size, chunk_size):
            for c in range(0, current_size, chunk_size):
                pattern = gen_pattern(grid, r, c, chunk_size)
                chunk2 = rules.pattern_to_grid(rules.transform(pattern))
                for i, row2 in enumerate(chunk2):
                    grid2[i + r2].extend(row2)
            r2 += len(chunk2)
        grid = grid2

    return sum([row.count('#') for row in grid])


def slurp(fname: str) -> list[str]:
    with open(fname) as file:
        return [line.rstrip() for line in file.readlines()]


def main():
    sample_input = slurp('input/sample_input.txt')
    main_input = slurp('input/input.txt')

    for inp in (main_input, ):
        rules = TransformRules(inp)
        print("Part 1 answer =", part1(rules, 5))
        print("Part 2 answer =", part1(rules, 18))
        print()


if __name__ == '__main__':
    main()
