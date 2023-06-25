#!/usr/bin/python3 -u

# Ergh! This can all be done using deque's rotate() method.
# TODO: rewrite using deque

class Node:
    def __init__(self, marble_num, left=None, right=None):
        # note: I'm unsure how to type hint this function...
        self.marble = marble_num
        self.left = left
        self.right = right


def show(start_node, pos) -> None:
    node = start_node
    while True:
        if node == pos:
            print(f'({node.marble}) ', end='')
        else:
            print(f'{node.marble} ', end='')
        node = node.right
        if node is start_node:
            break
    print()


def delete_node(node: Node) -> None:
    node.left.right = node.right
    node.right.left = node.left
    # del node


def insert_right(node: Node, marble: int) -> None:
    new_node = Node(marble)
    new_node.left = node
    new_node.right = node.right
    new_node.right.left = new_node
    node.right = new_node


def validate_doubly_linked_list(start_node: Node) -> bool:
    node = start_node
    while True:
        if node.left.right is not node:
            print(f'err: {node.marble} left side, {node.left.right.marble=}')
            return False
        if node.right.left is not node:
            print(f'err: {node.marble} right side, {node.right.left.marble=}')
            return False
        node = node.right
        if node is start_node:
            break
    return True


def part1(num_players: int, hi_marble: int) -> int:
    # start by initializing the first two nodes
    start_node = Node(0)
    start_node.left = start_node.right = start_node
    insert_right(start_node, 1)
    pos = start_node.right
    scores = [0] * (num_players + 1)
    player = 2

    for marble in range(2, hi_marble + 1):
        if marble % 23 == 0:
            for _ in range(7):
                pos = pos.left
            scores[player] += marble + pos.marble
            next_node = pos.right
            delete_node(pos)
            pos = next_node
        else:
            insert_right(pos.right, marble)
            pos = pos.right.right

        player += 1
        if player > num_players:
            player = 1

    return max(scores)


def part2(num_players: int, hi_marble: int) -> int:
    return part1(num_players, hi_marble * 100)


def main():
    inputs = ((9, 25), (10, 1618), (13, 7999), (17, 1104), (21, 6111),
              (30, 5807), (446, 71522))

    for num_players, hi_marble in inputs:
        print("Part 1 answer =", part1(num_players, hi_marble))
        print("Part 2 answer =", part2(num_players, hi_marble))
        print()


if __name__ == '__main__':
    main()
