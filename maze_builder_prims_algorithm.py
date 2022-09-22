import random
from random import randrange
from tkinter import *


def create_blank_maze(row_num, col_num):
    return_array = []
    for row in range(row_num):
        row_list = []
        for col in range(col_num):
            row_list.append(['u'])
        return_array.append(row_list)
    return return_array


def select_random_start_cell(row_num, col_num):
    # Pick random index for start cell
    row = 1 + randrange(row_num - 2)
    col = 1 + randrange(col_num - 2)

    return [row, col]


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

    return [[entry_y, 0], [exit_y, width - 1]]


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


def maze_creator(h, w):
    # define height and width
    height = h
    width = w

    unchecked_cells = [[i, j] for i in range(height) for j in range(width)]
    checked_cells = []
    wall_cell_list = []
    step_list = []

    # create blank maze
    maze = create_blank_maze(height, width)

    # Setting up the starting checked cell
    start_cell = select_random_start_cell(height, width)
    maze[start_cell[0]][start_cell[1]] = ['c']
    checked_cells.append(start_cell)
    # add to step list:
    step_list.append([start_cell, maze[start_cell[0]][start_cell[1]]])

    # Setting up the starting wall cells
    for wall_cell in get_adj_cells(height, width, start_cell):
        maze[wall_cell[0]][wall_cell[1]] = ['w']
        wall_cell_list.append(wall_cell)
        # Add to step list
        step_list.append([wall_cell, maze[wall_cell[0]][wall_cell[1]]])

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
            # Add to step list
            step_list.append([wall_cell, ['c']])
            adj_cells = get_adj_cells(height, width, wall_cell)
            for cell in adj_cells:
                if cell not in checked_cells and cell not in wall_cell_list:
                    wall_cell_list.append(cell)
                    maze[cell[0]][cell[1]] = ['w']
                    # Add to step list
                    step_list.append([cell, ['w']])
                    # update unchecked cell list
                    if cell in unchecked_cells:
                        unchecked_cells.remove(cell)

        wall_cell_list.remove(wall_cell)

    # Convert unvisited cells to walls
    for cell in unchecked_cells:
        x, y = cell[0], cell[1]
        wall_cell_list.append(cell)
        maze[x][y] = ['w']
        # Add to step list
        step_list.append([cell, ['w']])

    for cell in pick_entry_and_exit(height, width, maze):
        maze[cell[0]][cell[1]] = ['c']
        step_list.append([cell, ['c']])

    return [maze, step_list]


def get_width__and_height(canvas, w_entry, h_entry, check_var, master, build_maze_button):
    width_val = int(w_entry.get())
    height_val = int(h_entry.get())

    maze_vals = maze_creator(width_val, height_val)

    if check_var.get() == 0:
        draw_maze(canvas, maze_vals[0])
    else:
        build_maze_button['state'] = "disabled"
        animated_draw_maze(canvas, maze_vals[0], maze_vals[1], master, build_maze_button)


def draw_maze(canvas, maze):
    if len(maze) > len(maze[0]):
        box_w_divisor = len(maze)
    else:
        box_w_divisor = len(maze[0])

    box_w = 600 // box_w_divisor

    # Draw the actual maze in rectangles
    canvas.create_rectangle(0, 0, 600, 600, fill="white", outline="white")
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            if maze[row][col] == ['w']:
                canvas.create_rectangle(box_w * col, box_w * row, box_w * col + box_w, box_w * row + box_w,
                                        fill="blue", outline="black")
            elif maze[row][col] == ['c']:
                canvas.create_rectangle(box_w * col, box_w * row, box_w * col + box_w, box_w * row + box_w,
                                        fill="red", outline="black")
            else:
                canvas.create_rectangle(box_w * col, box_w * row, box_w * col + box_w, box_w * row + box_w,
                                        fill="grey", outline="black")


# Expected maze return format:
# [
# [maze array],
# [step_list]
# ]

# step_list format:
# [
# [[row, col], value], ...
# ]
def animated_draw_maze(canvas, maze, step_list, root, build_maze_button):
    row_num = len(maze)
    col_num = len(maze[0])

    if row_num > col_num:
        box_w_divisor = row_num
    else:
        box_w_divisor = col_num

    box_w = 600 // box_w_divisor

    blank_maze = create_blank_maze(row_num, col_num)

    draw_maze(canvas, blank_maze)

    add_box(canvas, box_w, step_list, root, build_maze_button)


def draw_box(canvas, box_w, row, col, color):
    canvas.create_rectangle(box_w * col, box_w * row, box_w * col + box_w, box_w * row + box_w,
                            fill=color, outline="black")


def add_box(canvas, box_w, step_list, root, build_maze_button):
    if not step_list:
        build_maze_button['state'] = "active"
        return
    row, col, val = step_list[0][0][0], step_list[0][0][1], step_list[0][1]
    if val == ['c']:
        color = "red"
    else:
        color = "blue"
    draw_box(canvas, box_w, row, col, color)
    root.after(10, lambda: add_box(canvas, box_w, step_list, root, build_maze_button))
    step_list = step_list[1:]


def only_numbers(char):
    return char.isdigit()


def create_gui():
    master = Tk()
    master.geometry(f'{600 + 225}x{600}')
    master.title("Maze Builder")

    # Validation Check
    validation = master.register(only_numbers)

    # Create canvas which will house the text elements for the GUI
    text_canvas = Canvas(master, width=100, height=300)
    text_canvas.pack(side="left")

    # Create title text
    text_canvas.create_text(50, 50, text="Maze Builder")

    # Create width and height entry fields and prompts
    text_canvas.create_text(60, 115, text="Maze Height: ")
    height_entry = Entry(master, validate="key", validatecommand=(validation, '%S'))
    height_entry.insert(END, '15')
    text_canvas.create_window(100, 140, window=height_entry)

    text_canvas.create_text(60, 175, text="Maze Width: ")
    width_entry = Entry(master, validate="key", validatecommand=(validation, '%S'))
    width_entry.insert(END, '15')
    text_canvas.create_window(100, 200, window=width_entry)

    # Create animate checkbox
    checked = IntVar()
    velocity_vector_checkbox = Checkbutton(master, text="Toggle Animation", onvalue=1, offvalue=0, variable=checked)
    velocity_vector_checkbox.place(x=80, y=375)

    # Create build maze button for input execution
    build_maze_button = Button(master, text="Build Maze", command=lambda: get_width__and_height(
        w, width_entry, height_entry, checked, master, build_maze_button))
    build_maze_button.place(x=100, y=400)

    # Create canvas which will house the maze animation
    w = Canvas(master, width=600, height=600)
    w.pack(side="right")

    # Draw the maze (is supposed to start out with a blank maze)
    draw_maze(w, create_blank_maze(15, 15))

    w.pack()
    master.mainloop()


def main():
    create_gui()


main()
