import math
import tkinter
import time

# width of the animation window
animation_window_width = 975
# height of the animation window
animation_window_height = 725
# initial x position of the ball
animation_ball_start_xpos = 50
# initial y position of the ball
animation_ball_start_ypos = 625
# radius of the ball
animation_ball_radius = 15
# the pixel movement of ball for each iteration
animation_ball_min_movement = 5
# delay between successive frames in seconds
animation_refresh_seconds = 0.01
# Meter to pixels
meter = 30
# time_elapsed_global = 0
zoom_counter = 0

# Empty x tick mark list
x_tick_marks = []
# Empty y tick mark list
y_tick_marks = []


def populate_x_ticks_initial(canvas):
    global x_tick_marks
    for i in range(100):
        if (i + 1) % 5 == 0:
            x_tick_marks.append(tkinter.Label(canvas, text=i + 1, width=2))


def populate_y_ticks_initial(canvas):
    global y_tick_marks
    for i in range(70):
        if (i + 1) % 5 == 0:
            y_tick_marks.append(tkinter.Label(canvas, text=i + 1, width=2))


# The main window of the animation
def create_animation_window():
    window = tkinter.Tk()
    window.title("Projectile Motion Simulator")
    # Uses python 3.6+ string interpolation
    window.geometry(f'{animation_window_width}x{animation_window_height + 225}')
    return window


# Create a canvas for animation and add it to main window
def create_animation_canvas(window):
    canvas = tkinter.Canvas(window)
    canvas.configure(bg="white")
    canvas.pack(fill="both", expand=True, side="top")
    canvas.create_line(0, animation_ball_start_ypos, animation_window_width, animation_ball_start_ypos)
    canvas.create_line(animation_ball_start_xpos, animation_window_height, animation_ball_start_xpos, 0)
    return canvas


def create_input_canvas(window):
    canvas = tkinter.Canvas(window)
    canvas.configure(bg="#457EAC")
    canvas.pack(fill="x", side="bottom")
    return canvas


def create_ball(canvas, start_x, start_height):
    ball_radius = meter / 2
    ball = canvas.create_oval(animation_ball_start_xpos - ball_radius + start_x,
                              animation_ball_start_ypos - ball_radius - start_height,
                              animation_ball_start_xpos + ball_radius + start_x,
                              animation_ball_start_ypos + ball_radius - start_height,
                              fill="#7777E4", outline="black", width=2)
    return ball


def my_round(x, base=5):
    return base * round(x / base)


def round_two_digits(text):
    text_val = str(round(text, 2))
    if len(text_val.split('.')[-1]) == 1:
        text_val += "0"
    return text_val


def create_velocity_vectors(canvas, coordinates, v, a, t, color="black"):
    xl, yl, xr, yr = coordinates
    x, y = (xl + xr) / 2, (yl + yr) / 2
    vy = v * math.sin(a) - 9.8 * t
    x_arrow = canvas.create_line(x, y, x + v * math.cos(a) * 10, y, arrow=tkinter.LAST, fill=color)
    y_arrow = canvas.create_line(x, y, x, y - vy * 10, arrow=tkinter.LAST, fill=color)
    return x_arrow, y_arrow


def create_timer_text(canvas, t):
    timer = canvas.create_text((animation_window_width - 75) / 2, 75, fill="black", font='Helvetica 24 bold',
                               text=round_two_digits(t) + "s")
    return timer


# Create and animate ball
def animate_ball(value_list, canvas):
    start_height = value_list[1] * meter
    ball = create_ball(canvas, 0, start_height)
    time_elapsed = 0
    prev_rounded_coordinate = 0
    x_arrow, y_arrow = 0, 0

    time_text = create_timer_text(canvas, time_elapsed)

    while True:
        # adjust timer
        canvas.delete(time_text)
        time_text = create_timer_text(canvas, time_elapsed)

        ball_pos = canvas.coords(ball)
        # unpack array to variables
        xl, yl, xr, yr = ball_pos

        time_elapsed += animation_refresh_seconds
        # time_elapsed_global += animation_refresh_seconds

        rounded_coordinate = my_round((((xl + xr) - 50) / 2))
        if rounded_coordinate % 20 == 0 and rounded_coordinate != prev_rounded_coordinate:
            create_dot(canvas, ball_pos)
            prev_rounded_coordinate = rounded_coordinate

        x_move = x_pos_pixels(calculate_x_pos(time_elapsed, value_list))
        y_move = x_pos_pixels(calculate_y_pos(time_elapsed, value_list))

        canvas.delete(ball)

        ball = create_ball(canvas, x_move, y_move)

        coordinates_display['text'] = "Coordinates: (" + round_two_digits(calculate_x_pos(time_elapsed, value_list)) + \
                                      "m, " + round_two_digits(calculate_y_pos(time_elapsed, value_list)) + "m)"

        # Creating velocity vectors
        canvas.delete(x_arrow)
        canvas.delete(y_arrow)
        if checked.get() == 1:
            x_arrow, y_arrow = create_velocity_vectors(canvas, ball_pos, value_list[0],
                                                       value_list[2], time_elapsed)
        else:
            x_arrow, y_arrow = create_velocity_vectors(canvas, ball_pos, value_list[0],
                                                       value_list[2], time_elapsed)
            canvas.itemconfigure(x_arrow, state='hidden')
            canvas.itemconfigure(y_arrow, state='hidden')

        canvas.update()
        time.sleep(animation_refresh_seconds)

        if xl > animation_window_width:
            canvas.delete(time_text)
            coordinates_display['text'] = "Coordinates: (" + round_two_digits(get_horizontal_distance(value_list)) + \
                                          "m, 0m)"
            break
        if (yr + yl) / 2 >= 625 and time_elapsed > get_time_in_flight(value_list) - 1:
            canvas.delete(time_text)
            coordinates_display['text'] = "Coordinates: (" + round_two_digits(get_horizontal_distance(value_list)) + \
                                          "m, 0m)"
            break


def calculate_y_pos(t, value_list):
    v, h, a = value_list
    return h + ((math.sin(a) * v) * t) + (
            0.5 * -9.8 * (t ** 2))


def calculate_x_pos(t, value_list):
    v, h, a = value_list
    return (math.cos(a) * v) * t


def x_pos_pixels(in_meters):
    return in_meters * meter


def y_pos_pixels(in_meters):
    return 625 - in_meters * meter


def draw_animation_background(canvas):
    canvas.create_line(0, animation_ball_start_ypos, animation_window_width, animation_ball_start_ypos)
    canvas.create_line(animation_ball_start_xpos, animation_window_height, animation_ball_start_xpos, 0)
    draw_axis_tik_marks(canvas)


def clear_prev_data_summary():
    max_height_label['text'] = "Max Height Reached: "
    time_to_max_height_label['text'] = "Time to Maximum Height: "
    horizontal_distance_label['text'] = "Distance Traveled: "
    time_in_flight_label['text'] = "Time in Flight: "


def fill_data_summary(value_list):
    max_height_label['text'] = "Max Height Reached: " + round_two_digits(get_maximum_height(value_list)) + " m"
    time_to_max_height_label['text'] = "Time to Maximum Height: " + \
                                       round_two_digits(round(get_max_h_time(value_list), 2)) + " s"
    horizontal_distance_label['text'] = "Distance Traveled: " + \
                                        round_two_digits(get_horizontal_distance(value_list)) + " m"
    time_in_flight_label['text'] = "Time in Flight: " + round_two_digits(get_time_in_flight(value_list)) + " s"


def launch_command(canvas):
    launch_button['state'] = "disabled"
    zoom_in_button['state'] = "disabled"
    zoom_out_button['state'] = "disabled"
    time_box.config(state='disabled')
    time_button.config(state='disabled')

    value_list = [init_velocity_slider.get(), init_height_slider.get(), init_launch_angle.get() * (math.pi / 180)]
    canvas.delete('all')
    pause_button.configure(command=pause_button_command)
    pause_button['text'] = "Pause"
    draw_animation_background(canvas)
    clear_prev_data_summary()
    animate_ball(value_list, canvas)
    fill_data_summary(value_list)
    create_timer_text(canvas, get_time_in_flight(value_list))
    draw_max_h_dot(value_list)

    launch_button['state'] = "normal"
    zoom_in_button['state'] = "normal"
    zoom_out_button['state'] = "normal"
    time_box.config(state='normal')
    time_button.config(state='normal')


def create_dot(canvas, coordinates, color_var=None, outline="black", radius=3):
    xl, yl, xr, yr = coordinates
    center_x, center_y = (xl + xr) / 2, (yl + yr) / 2
    xl, yl, xr, yr = center_x - radius, center_y - radius, center_x + radius, center_y + radius
    return canvas.create_oval(xl, yl, xr, yr, fill=color_var, outline=outline)


def height_adjust_command(h):
    launch_button['state'] = "normal"
    animation_canvas.delete('all')
    draw_animation_background(animation_canvas)
    pause_button.configure(command=pause_button_command)
    pause_button['text'] = "Pause"
    create_timer_text(animation_canvas, 0.00)
    create_ball(animation_canvas, 0, int(h) * meter)
    coordinates_display['text'] = "Coordinates: (0m, " + str(h) + "m)"


def draw_axis_tik_marks(canvas):
    global x_tick_marks
    # x_tick_marks = [tkinter.Label(animation_canvas, text=str(i*5)) for i in range(1, 20)]
    x_count = 0
    # for i in range(int((animation_window_width - 75) / meter)):
    for i in range(len(x_tick_marks) * 5):
        x_coordinate = animation_ball_start_xpos + (i + 1) * meter
        if (i + 1) % 5 == 0:
            lower_y = animation_ball_start_ypos + 15
            upper_y = animation_ball_start_ypos - 15
            canvas.create_line(x_coordinate, upper_y, x_coordinate, 0, fill="light grey")
            x_tick_marks[x_count].place(x=x_coordinate - 12, y=animation_ball_start_ypos + 20)
            x_count += 1

        else:
            lower_y = animation_ball_start_ypos + 8
            upper_y = animation_ball_start_ypos - 8
        canvas.create_line(x_coordinate, lower_y, x_coordinate, upper_y)

    y_count = 0
    for i in range(len(y_tick_marks) * 5):
        y_coordinate = animation_ball_start_ypos - (i + 1) * meter
        if (i + 1) % 5 == 0:
            left_x = animation_ball_start_xpos - 15
            right_x = animation_ball_start_xpos + 15
            canvas.create_line(right_x, y_coordinate, animation_window_width, y_coordinate, fill="light grey")
            y_tick_marks[y_count].place(x=left_x - 30, y=y_coordinate - 12)
            y_count += 1
        else:
            left_x = animation_ball_start_xpos - 8
            right_x = animation_ball_start_xpos + 8
        canvas.create_line(left_x, y_coordinate, right_x, y_coordinate)


def get_time_in_flight(value_list):
    v, h, a = value_list
    if v == 0 or (h + a == 0):
        return 0
    else:
        option1 = ((-v * math.sin(a)) + math.sqrt((v * math.sin(a)) ** 2 - 4 * -4.9 * h)) / -9.8
        option2 = ((-v * math.sin(a)) - math.sqrt((v * math.sin(a)) ** 2 - 4 * -4.9 * h)) / -9.8
        return round(max(option1, option2), 2)


def get_max_h_time(value_list):
    v, h, a = value_list
    return (v * math.sin(a)) / 9.8


def get_maximum_height(value_list):
    v, h, a = value_list
    derived_t = get_max_h_time(value_list)
    max_height = h + (v * math.sin(a)) * derived_t + 0.5 * -9.8 * (derived_t ** 2)
    return round(max_height, 2)


def draw_max_h_dot(value_list):
    center_x = x_pos_pixels(calculate_x_pos(get_max_h_time(value_list), value_list)) + 50
    center_y = y_pos_pixels(get_maximum_height(value_list))
    coordinates = [center_x - 3, center_y - 3, center_x + 3, center_y + 3]
    return create_dot(animation_canvas, coordinates, color_var="Red", outline="Red", radius=5)


def get_horizontal_distance(value_list):
    v, h, a = value_list
    return round(get_time_in_flight(value_list) * v * math.cos(a), 2)


def pause_button_command():
    pause_button['text'] = "Resume"
    pause_button.configure(command=play_button_command)
    animation_canvas.update()
    text_var = "Resume"

    while text_var == "Resume":
        time.sleep(animation_refresh_seconds)
        animation_canvas.update()
        text_var = pause_button['text']


def play_button_command():
    pause_button['text'] = "Pause"
    pause_button.configure(command=pause_button_command)


def zoom_in_command():
    global zoom_counter
    global meter
    global x_tick_marks

    if zoom_counter >= -3:
        zoom_out_button['state'] = 'normal'
    if zoom_counter == 2:
        zoom_in_button['state'] = 'disable'

    meter *= 1.5
    zoom_counter += 1
    animation_canvas.delete('all')
    # draw_animation_background(animation_canvas)
    height_adjust_command(init_height_slider.get())

    #x_tick_marks[0].config(state="disabled")
    # if zoom_counter == 3:
    #   zoom_in_button['state'] = 'disable'


def zoom_out_command():
    global zoom_counter
    global meter

    if zoom_counter <= 3:
        zoom_in_button['state'] = 'normal'

    if zoom_counter == -2:
        zoom_out_button['state'] = 'disable'

    meter *= (2/3)
    zoom_counter -= 1
    animation_canvas.delete('all')
    # draw_animation_background(animation_canvas)
    height_adjust_command(init_height_slider.get())


# def create_instant_trace_path(canvas, value_list, time_value):
def create_instant_trace_path(time_value, radius=3):
    value_list = [init_velocity_slider.get(), init_height_slider.get(), init_launch_angle.get() * (math.pi / 180)]
    time_value = int(time_value*100)
    # prev_x = 65
    for i in range(0, time_value, 10):
        i /= 100
        x_pos = 50 + x_pos_pixels(calculate_x_pos(i, value_list))
        y_move = y_pos_pixels(calculate_y_pos(i, value_list))
        [xl, yl, xr, yr] = x_pos - radius, y_move - radius, x_pos + radius, y_move + radius
        create_dot(animation_canvas, [xl, yl, xr, yr])


def see_specific_time():
    collected_time = float(time_box.get("1.0", "end-1c"))
    value_list = [init_velocity_slider.get(), init_height_slider.get(), init_launch_angle.get() * (math.pi / 180)]

    if collected_time > get_time_in_flight(value_list):
        collected_time = get_time_in_flight(value_list)
    elif collected_time < 0:
        collected_time = 0

    animation_canvas.delete('all')
    draw_animation_background(animation_canvas)
    create_timer_text(animation_canvas, round(collected_time, 2))

    x_pos = x_pos_pixels(calculate_x_pos(collected_time, value_list))
    y_move = y_pos_pixels(calculate_y_pos(collected_time, value_list))

    create_instant_trace_path(collected_time)
    create_ball(animation_canvas, x_pos, animation_ball_start_ypos-y_move)

    coordinates_display['text'] = "Coordinates: (" + str(round(calculate_x_pos(collected_time, value_list), 2)) + \
                                  "m, " + str(round(calculate_y_pos(collected_time, value_list), 2)) + "m)"

    return None


# The actual execution starts here
animation_window = create_animation_window()
animation_canvas = create_animation_canvas(animation_window)
input_canvas = create_input_canvas(animation_window)
time_text = create_timer_text(animation_canvas, 0.00)

populate_x_ticks_initial(animation_canvas)
populate_y_ticks_initial(animation_canvas)

draw_axis_tik_marks(animation_canvas)
create_ball(animation_canvas, 0, 0)


# Add elements to input canvas
init_velocity_slider = tkinter.Scale(input_canvas, label="Initial Velocity", from_=0, to=30, orient=tkinter.HORIZONTAL,
                                     length=260, tickinterval=5)
init_velocity_slider.grid(row=0, column=0, pady=20, padx=20)

init_height_slider = tkinter.Scale(input_canvas, label="Initial Height", from_=0, to=15, orient=tkinter.HORIZONTAL,
                                   length=260, tickinterval=3, command=height_adjust_command)
init_height_slider.grid(row=0, column=1)

init_launch_angle = tkinter.Scale(input_canvas, label="Launch Angle", from_=0, to=90, orient=tkinter.HORIZONTAL,
                                  length=260, tickinterval=15)
init_launch_angle.grid(row=0, column=2, padx=20)

launch_button = tkinter.Button(input_canvas, text="Launch!", command=lambda: launch_command(animation_canvas))
launch_button.grid(row=0, column=3, sticky="NS", pady=20)

# Creating Data Summary Page
tkinter.Label(input_canvas, text="Data Summary:", font='Helvetica 18 bold').grid(row=1, column=0, padx=20, pady=5)

max_height_label = tkinter.Label(input_canvas, text="Max Height Reached:")
max_height_label.grid(row=2, column=0, padx=30)

time_to_max_height_label = tkinter.Label(input_canvas, text="Time to Maximum Height:")
time_to_max_height_label.grid(row=3, column=0, padx=30)

horizontal_distance_label = tkinter.Label(input_canvas, text="Distance Traveled:")
horizontal_distance_label.grid(row=4, column=0, padx=30)

time_in_flight_label = tkinter.Label(input_canvas, text="Time in Flight:")
time_in_flight_label.grid(row=5, column=0, padx=30)

time_prompt = tkinter.Label(input_canvas, text="Time: (s)")
time_prompt.grid(row=1, column=1, sticky="W")

time_box = tkinter.Text(input_canvas, height=1, width=27)
time_box.grid(row=1, column=1, sticky="E")

time_button = tkinter.Button(input_canvas, height=1, width=27, text="See Projectile Position",
                             command=see_specific_time)
time_button['width'] = 18
time_button.grid(row=2, column=1, sticky="EW")

coordinates_display = tkinter.Label(input_canvas, text="Coordinates: (0m, 0m)")
coordinates_display.grid(row=3, column=2)

checked = tkinter.IntVar()
velocity_vector_checkbox = tkinter.Checkbutton(input_canvas, text="Show Velocity Vectors",
                                               variable=checked, onvalue=1, offvalue=0)
velocity_vector_checkbox.grid(row=1, column=2, padx=30)

pause_button = tkinter.Button(input_canvas, text="Pause", command=pause_button_command)
pause_button.grid(row=1, column=3, sticky="NS" + "EW")

zoom_in_button = tkinter.Button(input_canvas, text="Zoom In", command=zoom_in_command)
zoom_in_button.grid(row=3, column=3, sticky="EW")

zoom_out_button = tkinter.Button(input_canvas, text="Zoom Out", command=zoom_out_command)
zoom_out_button.grid(row=4, column=3, sticky="EW")

animation_window.mainloop()
