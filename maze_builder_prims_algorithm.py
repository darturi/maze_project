import random
from random import randrange


def create_blank_maze(row_num, col_num):
    return_array = []
    for row in range(row_num):
        row_list = []
        for col in range(col_num):
            row_list.append(['u'])
        return_array.append(row_list)
    return return_array


def select_random_start_cell(height, width):
    # Pick random index for start cell
    x_coordinate = 1 + randrange(height - 2)
    y_coordinate = 1 + randrange(width - 2)

    return [x_coordinate, y_coordinate]


# Checks if the cell passed in as the third parameter is a border
def check_if_border(height, width, cell):
    x, y = cell[0], cell[1]
    if x == 0 or x == height - 1 or y == 0 or y == width - 1:
        # Returns true if the cell is in fact a border cell
        return True
    # Returns false if the cell is not a border cell
    return False


def get_adj_cells(height, width, cell, previously_checked_walls=[]):
    x, y = cell[0], cell[1]

    # Creates a list of all cells adjacent to the one passed in as input
    adj_cell_list = [[x, y - 1], [x, y + 1], [x - 1, y], [x + 1, y]]

    # Remove all the cells that are adjacent to the original cell but are walls
    non_border_cells = []
    for i in adj_cell_list:
        if not check_if_border(height, width, i) and i not in previously_checked_walls:
            non_border_cells.append(i)

    # return the results of the calculations of the function
    return non_border_cells


def pick_entry_and_exit(height, width, maze):
    entry_y = -1
    exit_y = -1

    while maze[entry_y][1] != ['c']:
        entry_y = 1 + randrange(height - 2)

    while maze[exit_y][width - 2] != ['c']:
        exit_y = 1 + randrange(height - 2)

    return [[entry_y, 0], [exit_y, width-1]]


# Returns True if wall divides two visited cells or False if not
# (if it's False delete the wall)
def check_wall_division(wall_cell, maze):
    x, y = wall_cell[0], wall_cell[1]

    # Creates a list of all cells adjacent to the one passed in as input
    adj_cells = [[x, y - 1], [x, y + 1], [x - 1, y], [x + 1, y]]

    checked_count = 0
    unchecked_count = 0
    for cell in adj_cells:
        if maze[cell[0]][cell[1]] == ['c']:
            checked_count += 1
        elif maze[cell[0]][cell[1]] == ['u']:
            unchecked_count += 1

    if checked_count < 2 and unchecked_count > 1:
        return False
    return True


def maze_creator():
    # define height and width
    height = 10
    width = 10

    unchecked_cells = [[i, j] for i in range(width) for j in range(height)]
    checked_cells = []
    wall_cell_list = []

    # create blank maze
    maze = create_blank_maze(height, width)

    # Setting up the starting checked cell
    start_cell = select_random_start_cell(height, width)
    maze[start_cell[0]][start_cell[1]] = ['c']
    checked_cells.append(start_cell)

    # Setting up the starting wall cells
    for wall_cell in get_adj_cells(height, width, start_cell):
        maze[wall_cell[0]][wall_cell[1]] = ['w']
        wall_cell_list.append(wall_cell)

    # update unchecked cell list
    unchecked_cells.remove(start_cell)
    for cell in wall_cell_list:
        unchecked_cells.remove(cell)

    while len(wall_cell_list) > 0:
        wall_cell = random.choice(wall_cell_list)
        check_div = check_wall_division(wall_cell, maze)

        if not check_div:
            checked_cells.append(wall_cell)
            maze[wall_cell[0]][wall_cell[1]] = ['c']
            adj_cells = get_adj_cells(height, width, wall_cell)
            for cell in adj_cells:
                if cell not in checked_cells and cell not in wall_cell_list:
                    wall_cell_list.append(cell)
                    maze[cell[0]][cell[1]] = ['w']

                    # update unchecked cell list
                    if cell in unchecked_cells:
                        unchecked_cells.remove(cell)

        wall_cell_list.remove(wall_cell)

    # Convert unvisited cells to walls
    for cell in unchecked_cells:
        x, y = cell[0], cell[1]
        wall_cell_list.append(cell)
        maze[x][y] = ['w']

    for cell in pick_entry_and_exit(height, width, maze):
        maze[cell[0]][cell[1]] = ['c']

    return maze


def main():
    for i in maze_creator():
        print(i)


main()
