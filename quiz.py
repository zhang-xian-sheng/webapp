#!/usr/bin/env python3
# --*-- coding: utf-8 --*--


def reverse_list(l: list):
    """

    TODO: Reverse a list without using any built in functions



    The function should return a sorted list.

    Input l is a list which can contain any type of data.

    """
    reversed_list = []
    for i in range(len(l) - 1, -1, -1):
        reversed_list.append(l[i])
    return reversed_list


def solve_sudoku(matrix):
    """

    TODO: Write a programme to solve 9x9 Sudoku board.



    Sudoku is one of the most popular puzzle games of all time. The goal of Sudoku is to fill a 9×9 grid with numbers so that each row, column and 3×3 section contain all of the digits between 1 and 9. As a logic puzzle, Sudoku is also an excellent brain game.



    The input matrix is a 9x9 matrix. You need to write a program to solve it.

    """
    # set the empty position to ""
    # row col block num list
    row = [set(range(1, 10)) for _ in range(9)]
    col = [set(range(1, 10)) for _ in range(9)]
    block = [set(range(1, 10)) for _ in range(9)]

    # empty position list
    empty_positions = []
    for i in range(9):
        for j in range(9):
            # set available number
            if matrix[i][j] != '':
                val = int(matrix[i][j])
                row[i].remove(val)
                col[j].remove(val)
                block[(i // 3) * 3 + j // 3].remove(val)
            else:
                empty_positions.append((i, j))

    def backtrack(iterm=0):
        if iterm == len(empty_positions):
            return True
        i, j = empty_positions[iterm]
        b = (i // 3) * 3 + j // 3
        for val in row[i] & col[j] & block[b]:
            row[i].remove(val)
            col[j].remove(val)
            block[b].remove(val)
            matrix[i][j] = str(val)
            if backtrack(iterm + 1):
                return True
            row[i].add(val)  # 回溯
            col[j].add(val)
            block[b].add(val)
        return False

    backtrack()
