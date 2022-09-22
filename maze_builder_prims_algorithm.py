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


def get_adj_cells(height, width, cell):
    x, y = cell[0], cell[1]

    # Creates a list of all cells adjacent to the one passed in as input
    adj_cell_list = [[x, y - 1], [x, y + 1], [x - 1, y], [x + 1, y]]

    # Remove all the cells that are adjacent to the original cell but are walls and return
    return [i for i in adj_cell_list if not check_if_border(height, width, i)]


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


def maze_creator(height, width):
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


# Executes maze graphical representation protocols
def execute_maze_representation(canvas, w_entry, h_entry, check_var, master, build_maze_button):
    # collect width and height values from entry fields
    width_val, height_val = int(w_entry.get()), int(h_entry.get())

    # Create a maze and a step_list
    maze_vals = maze_creator(width_val, height_val)

    # Toggle animation is not checked just make a maze
    if check_var.get() == 0:
        draw_maze(canvas, maze_vals[0])
    # Toggle animation is checked animate the process of making the same maze
    else:
        # Disable the build_maze_button until the animation is done running (happens in the below function)
        build_maze_button['state'] = "disabled"
        animated_draw_maze(canvas, maze_vals[0], maze_vals[1], master, build_maze_button)


# Finds the greater of the two dimensions inputted (height or width) and then divides 600 by that value as to provide
# an appropriate pixel count for the width (and by extension) height of a single cell in the generated grid
def get_box_w(maze):
    row_num, col_num = len(maze), len(maze[0])
    if row_num > col_num:
        box_w_divisor = row_num
    else:
        box_w_divisor = col_num

    return 600 // box_w_divisor


def draw_maze(canvas, maze):
    # Calculate appropriate dimensions for a single cell in the grid
    box_w = get_box_w(maze)

    # Create a background square
    canvas.create_rectangle(0, 0, 600, 600, fill="white", outline="white")

    # Draw the actual maze in rectangles
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            if maze[row][col] == ['w']:
                draw_box(canvas, box_w, row, col, "blue")
            elif maze[row][col] == ['c']:
                draw_box(canvas, box_w, row, col, "red")
            else:
                draw_box(canvas, box_w, row, col, "grey")


def animated_draw_maze(canvas, maze, step_list, root, build_maze_button):
    row_num, col_num = len(maze), len(maze[0])

    # Calculate appropriate dimensions for a single cell in the grid
    box_w = get_box_w(maze)

    # Set a blank canvas so that the new maze is not drawn over a previously existing maze
    draw_maze(canvas, create_blank_maze(row_num, col_num))

    # Call the add_bix function for the first time (will proceed to call itself recursively)
    add_box(canvas, box_w, step_list, root, build_maze_button)


# A function that will draw a single cell of the maze grid based on its position in the array as well as its value
def draw_box(canvas, box_w, row, col, color):
    canvas.create_rectangle(box_w * col, box_w * row, box_w * col + box_w, box_w * row + box_w,
                            fill=color, outline="black")


# Function that recursively calls itself in order to animate the process of building the maze as based on a list
# returned from the maze_creator() function that documents the process in which the maze was created step by step
# (obviously chronologically)
def add_box(canvas, box_w, step_list, root, build_maze_button):
    # If step_list is empty (all items have gradually been removed) then return as to exit the recursion process
    if not step_list:
        build_maze_button['state'] = "active"
        return
    row, col, val = step_list[0][0][0], step_list[0][0][1], step_list[0][1]
    if val == ['c']:
        draw_box(canvas, box_w, row, col, "red")
    else:
        draw_box(canvas, box_w, row, col, "blue")

    # The below line is what determines the delay between when each square of the grid is added to the GUI
    root.after(10, lambda: add_box(canvas, box_w, step_list, root, build_maze_button))
    # Deletes the added square from step_list
    step_list = step_list[1:]


# This function is made to disallow any non-integer inputs into the entry fields
def only_numbers(char):
    return char.isdigit()


# Creates and manages the foundation and framework of the GUI
def create_gui():
    master = Tk()
    master.geometry(f'{600 + 225}x{600}')
    master.title("Maze Builder")

    # Validation Check for entry input values
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
    build_maze_button = Button(master, text="Build Maze", command=lambda: execute_maze_representation(
        w, width_entry, height_entry, checked, master, build_maze_button))
    build_maze_button.place(x=100, y=400)

    # Create canvas which will house the maze animation
    w = Canvas(master, width=600, height=600)
    w.pack(side="right")

    # Draw the maze (starts out with a blank maze)
    draw_maze(w, create_blank_maze(15, 15))

    w.pack()
    master.mainloop()


def main():
    create_gui()


main()
