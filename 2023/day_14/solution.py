import cProfile
from enum import Enum
from typing import TypeVar

from utils_anviks.decorators import read_data, stopwatch

_T = TypeVar("_T")


@read_data('data.txt', sep2='')
@stopwatch
def solution(data: list[list[str]], part: int):
    """
    Solution for the day 14 problem.

    For part 1, return the total load of the rocks after 1 tilt to the north.
    For part 2, return the total load of the rocks after 1_000_000_000 cycles of tilting (north, west, south, east).
    :param data: The rocks from the input file.
    :param part: The part of the problem to solve.
    :return: The solution for the given part.
    """
    if part == 1:
        tilt_north(data)

        return calculate_total_load(data)
    else:
        total_loads = []

        for i in range(200):
            tilt_cycle(data)
            total_loads.append(calculate_total_load(data))

        cycle = find_cycle(total_loads)

        return cycle[(1_000_000_000 - len(total_loads) - 1) % len(cycle)]


def calculate_total_load(rocks):
    """
    Calculate the total load of the rocks.

    The load of one O-rock is equal to the number of rows below it + 1,
    meaning that if there are 10 rows of rocks, a rock in the 1st row (from the top) has a load of 10
    and a rock in the 10th row has a load of 1.
    :param rocks: The rocks.
    :return: The total load of the rocks.
    """
    load = 0

    for i, line in enumerate(rocks):
        load += (len(rocks) - i) * line.count('O')

    return load


def _find_cycle_helper(sequence: list[_T], window_size: int) -> list[_T] | None:
    window_1 = sequence[-window_size:]
    window_2 = sequence[-window_size * 2: -window_size]
    return window_1 if window_1 == window_2 else None


def find_cycle(sequence: list[_T]) -> list[_T] | None:
    result = None

    for i in range(2, len(sequence) // 2 + 1):
        result = _find_cycle_helper(sequence, i)
        if result:
            return result

    return result


def tilt_cycle(rocks: list[list[str]]) -> None:
    tilt_north(rocks)
    tilt_west(rocks)
    tilt_south(rocks)
    tilt_east(rocks)


def tilt_north(rocks: list[list[str]]) -> None:
    for j in range(len(rocks[0])):
        obstacle_index = -1
        for i in range(len(rocks)):
            rock = rocks[i][j]

            match rock:
                case 'O':
                    if obstacle_index + 1 == i:
                        obstacle_index += 1
                    else:
                        rocks[obstacle_index + 1][j] = 'O'
                        obstacle_index += 1
                        rocks[i][j] = '.'
                case '#':
                    obstacle_index = i


def tilt_south(rocks: list[list[str]]) -> None:
    for j in range(len(rocks[0])):
        obstacle_index = len(rocks[0])
        for i in range(len(rocks) - 1, -1, -1):
            rock = rocks[i][j]

            match rock:
                case 'O':
                    if obstacle_index - 1 == i:
                        obstacle_index -= 1
                    else:
                        rocks[obstacle_index - 1][j] = 'O'
                        obstacle_index -= 1
                        rocks[i][j] = '.'
                case '#':
                    obstacle_index = i


def tilt_west(rocks: list[list[str]]) -> None:
    for i in range(len(rocks)):
        obstacle_index = -1
        for j in range(len(rocks[0])):
            rock = rocks[i][j]

            match rock:
                case 'O':
                    if obstacle_index + 1 == j:
                        obstacle_index += 1
                    else:
                        rocks[i][obstacle_index + 1] = 'O'
                        obstacle_index += 1
                        rocks[i][j] = '.'
                case '#':
                    obstacle_index = j


def tilt_east(rocks: list[list[str]]) -> None:
    for i in range(len(rocks)):
        obstacle_index = len(rocks)
        for j in range(len(rocks[0]) - 1, -1, -1):
            rock = rocks[i][j]

            match rock:
                case 'O':
                    if obstacle_index - 1 == j:
                        obstacle_index -= 1
                    else:
                        rocks[i][obstacle_index - 1] = 'O'
                        obstacle_index -= 1
                        rocks[i][j] = '.'
                case '#':
                    obstacle_index = j


if __name__ == '__main__':
    print(solution(1))  # 107142   0.0008464003913104534 seconds
    print(solution(2))  # 104815   0.6032655001617968 seconds
