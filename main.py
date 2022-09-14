#!/usr/bin/python3

############################################################################################################
# Python Modules #
############################################################################################################
import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.font as tkFont
import numpy as np
# import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
import threading as tr
# import multiprocessing as mp
from datetime import datetime
import time as t

import commands
import command_descriptions
import constants
import globals
import myserial

command = commands.Commands()
command_description = command_descriptions.CommandDescriptions()
const = constants.Constants()
globe = globals.Globals()
serial_com = myserial.Serial()

############################################################################################################
# Window Construction #
############################################################################################################
main_window = tk.Tk()
main_window.geometry("610x700")
main_window.title('ESPROS epc901')

tabs = ttk.Notebook(main_window)

serial_tab = ttk.Frame(tabs)
epc901_configuration_tab = ttk.Frame(tabs)
plotting_tab = ttk.Frame(tabs)

tabs.add(serial_tab, text='Serial')
tabs.add(epc901_configuration_tab, text='Configuration')
tabs.add(plotting_tab, text='Plots')
tabs.pack(expand=1, fill="both")

# Serial Configuration Frame
serial_config_frame = Frame(serial_tab)
serial_config_frame.grid(row=0,
                         column=0)

# epc901 Configuration
epc901_config_frame = Frame(epc901_configuration_tab)
epc901_config_frame.grid(row=0,
                         column=0)

serial_monitor_frame = Frame(epc901_configuration_tab)
serial_monitor_frame.grid(row=1,
                          column=0)

serial_monitor_options_frame = Frame(epc901_configuration_tab)
serial_monitor_options_frame.grid(row=2,
                                  column=0)

# Plotting
plot_frame = Frame(plotting_tab)
plot_frame.grid(row=0,
                column=0)

plot_controls_frame = Frame(plotting_tab)
plot_controls_frame.grid(row=1,
                         column=0)

plot_control_buttons_frame = Frame(plot_controls_frame)
plot_control_buttons_frame.grid(row=0,
                                column=0)

plot_control_entries_frame = Frame(plot_controls_frame)
plot_control_entries_frame.grid(row=0,
                                column=1)

# Font Tuples
SECTION_LABEL_FONT = tkFont.Font(family="Ubuntu Mono",
                                 size=14,
                                 weight="bold",
                                 underline=True)

OPTION_FONT = tkFont.Font(family="FreeSans",
                          size=12,
                          weight="normal",
                          underline=True)

SUB_OPTION_FONT = tkFont.Font(family="FreeSans",
                              size=8,
                              weight="bold",
                              underline=False)

BUTTON_LABEL_FONT = tkFont.Font(family="saab",
                                size=8,
                                weight="normal",
                                underline=False)

# Global Variables #####################################################################################################
############
# Graphing #
############


########################################################################################################################

########################################################################################################################
# Serial Port Config #
########################################################################################################################
# Serial Port Configuration Label ######################################################################################
serial_configuration_label = ttk.Label(serial_config_frame,
                                       text="Serial Port Configuration",
                                       font=SECTION_LABEL_FONT)

serial_configuration_label.grid(columnspan=2,
                                column=0,
                                row=0,
                                padx=const.X_COLUMN_PAD,
                                pady=const.Y_SECTION_PAD)
########################################################################################################################

# Baudrate #############################################################################################################
baudrate_label = ttk.Label(serial_config_frame,
                           text="Select Baudrate:",
                           font=OPTION_FONT)

baudrate_label.grid(column=0,
                    row=1,
                    padx=const.X_COLUMN_PAD,
                    pady=const.Y_OPTION_PAD,
                    stick='w')

serial_baudrate_selected = ttk.Combobox(serial_config_frame,
                                        width=8,
                                        state='readonly')

serial_baudrate_selected['values'] = (
    '300', '1200', '2400', '4800', '9600', '19200', '38400', '57600', '74880', '115200', '230400', '250000', '500000',
    '1000000', '2000000')

serial_baudrate_selected.grid(column=1,
                              row=1,
                              padx=const.X_COLUMN_PAD,
                              pady=const.Y_OPTION_PAD,
                              stick='e')

serial_baudrate_selected.current(11)  # 250000 is default baudrate for the controller
########################################################################################################################

# Port Selection #######################################################################################################
gantry_port_sel_label = ttk.Label(serial_config_frame,
                                  text="Select Port:",
                                  font=OPTION_FONT)

gantry_port_sel_label.grid(column=0,
                           row=2,
                           padx=const.X_COLUMN_PAD,
                           pady=const.Y_OPTION_PAD,
                           stick='w')


def update_ports():  # Update port list every time the dropdown list is accessed
    serial_port_selected['values'] = serial_com.find_available_serial_ports()


serial_port_selected = ttk.Combobox(serial_config_frame,
                                    width=12,
                                    postcommand=update_ports,
                                    state='readonly')

serial_port_selected.grid(column=1,
                          row=2,
                          padx=const.X_COLUMN_PAD,
                          pady=const.Y_OPTION_PAD,
                          stick='e')


########################################################################################################################

# Connect button #######################################################################################################
def serial_connect_button_click():
    if not serial_com.port_open:
        serial_com.serial_port = serial_port_selected.get()
        serial_com.baud_rate = serial_baudrate_selected.get()
        print_to_serial_monitor("Trying to open port " +
                                serial_com.serial_port +
                                " at " +
                                serial_com.baud_rate +
                                " baud")
        serial_com.open_serial_port()

        # Start serial port monitor thread.
        # This pulls incoming data from the serial port
        # and prints it on the serial monitor
        if globe.BG_SERIAL_PORT_MONITOR_THREAD is None:
            globe.BG_SERIAL_PORT_MONITOR_THREAD = tr.Thread(target=background_serial_port_monitor)
            globe.BG_SERIAL_PORT_MONITOR_THREAD.start()

        if serial_com.port_open:
            print_to_serial_monitor("Connected!")

            # Change Connect button to show successful connection.
            connect_serial_button.configure(text="Connected!",
                                            bg="green")

            # Enable Reset Controller Button
            reset_controller_button.configure(state="normal",
                                              bg="#d46707")


connect_serial_button = tk.Button(serial_config_frame,
                                  text="Connect",
                                  command=lambda: serial_connect_button_click(),
                                  font=BUTTON_LABEL_FONT,
                                  bg="#326c88",
                                  fg="white",
                                  height=1,
                                  width=9)

connect_serial_button.grid(column=1,
                           row=3,
                           padx=const.X_COLUMN_PAD,
                           pady=const.Y_BUTTON_PAD,
                           stick='e')


########################################################################################################################

# Disconnect Button ####################################################################################################
def serial_disconnect_button_click():
    if serial_com.port_open:
        print_to_serial_monitor(serial_com.serial_port + " closed. ")
        serial_com.close_serial_port()

        # Revert Connect button
        connect_serial_button.configure(text="Connect",
                                        bg="#326c88")

        # Disable Reset Controller Button
        reset_controller_button.configure(state="disabled",
                                          bg="gray")


serial_disconnect_button = tk.Button(serial_config_frame,
                                     text="Disconnect",
                                     command=lambda: serial_disconnect_button_click(),
                                     font=BUTTON_LABEL_FONT,
                                     bg="#ba2121",
                                     fg="white",
                                     height=1,
                                     width=12)

serial_disconnect_button.grid(column=0,
                              row=3,
                              padx=const.X_COLUMN_PAD,
                              pady=const.Y_BUTTON_PAD,
                              stick='w')


########################################################################################################################

# Reset Controller Button ##############################################################################################
def reset_controller_button_click():
    if serial_com.port_open:
        serial_com.reset_controller()
        serial_com.begin = False
        print_to_serial_monitor("Controller Reset.")


reset_controller_button = tk.Button(serial_config_frame,
                                    text="Reset Controller",
                                    command=lambda: reset_controller_button_click(),
                                    font=BUTTON_LABEL_FONT,
                                    bg="#d46707",
                                    fg="white",
                                    height=1)

reset_controller_button.grid(columnspan=2,
                             row=4,
                             padx=const.X_COLUMN_PAD,
                             pady=const.Y_BUTTON_PAD)

reset_controller_button.configure(state="disabled",
                                  bg="gray")

########################################################################################################################

########################################################################################################################
# Configuration Commands Frame #########################################################################################
########################################################################################################################
configuration_commands_label = ttk.Label(epc901_config_frame,
                                         text="epc901 Configuration Commands",
                                         font=SECTION_LABEL_FONT)

configuration_commands_label.grid(columnspan=2,
                                  row=0,
                                  padx=const.X_COLUMN_PAD,
                                  pady=const.Y_OPTION_PAD)

# Command Description ##################################################################################################
command_description_label = ttk.Label(epc901_config_frame,
                                      text="Command Description:",
                                      font=OPTION_FONT)

command_description_label.grid(column=0,
                               row=1,
                               padx=const.X_COLUMN_PAD,
                               pady=const.Y_OPTION_PAD,
                               stick='w')

command_description_selected = ttk.Combobox(epc901_config_frame,
                                            width=22,
                                            state='readonly')

command_description_selected['values'] = ("Binning",
                                          "Amplifier gain",
                                          "Region of Interest (ROI)",
                                          "Read Direction",
                                          "Video Amplifier Bandwidth",
                                          "Various Settings",
                                          "Oscillator Trimming",
                                          "Temperature Sensors",
                                          "Analog Control Settings",
                                          "I2C Error Flag",
                                          "Chip Revision",
                                          "Software Reset")

command_description_selected.grid(column=1,
                                  row=1,
                                  padx=const.X_COLUMN_PAD,
                                  pady=const.Y_OPTION_PAD,
                                  stick='e')

command_description_selected.current(0)
########################################################################################################################

# Command Description Output Box #######################################################################################
command_description_box = tk.Text(epc901_config_frame,
                                  height=12,
                                  bg="#ABB8C3",
                                  # width=40,
                                  font=("Times New Roman", 9),
                                  padx=const.X_COLUMN_PAD,
                                  pady=const.Y_OPTION_PAD)

command_description_box.grid(columnspan=2,
                             row=2,
                             padx=const.X_COLUMN_PAD,
                             stick='ew')

command_description_box_scrollbar = tk.Scrollbar(epc901_config_frame,
                                                 orient='vertical',
                                                 command=command_description_box.yview)

command_description_box_scrollbar.grid(column=1,
                                       row=2,
                                       padx=const.X_COLUMN_PAD,
                                       sticky='nse')
command_description_box['yscrollcommand'] = command_description_box_scrollbar.set


def update_command_description_box(description):
    command_description_box.configure(state='normal')

    if description == "Binning":
        command_description_box.delete("1.0", "end")
        command_description_box.insert(tk.END, command_description.BINNING)

    elif description == "Amplifier gain":
        command_description_box.delete("1.0", "end")
        command_description_box.insert(tk.END, command_description.AMPLIFIER_GAIN)

    elif description == "Region of Interest (ROI)":
        command_description_box.delete("1.0", "end")
        command_description_box.insert(tk.END, command_description.ROI)

    elif description == "Read Direction":
        command_description_box.delete("1.0", "end")
        command_description_box.insert(tk.END, command_description.READ_DIRECTION)

    elif description == "Video Amplifier Bandwidth":
        command_description_box.delete("1.0", "end")
        command_description_box.insert(tk.END, command_description.VIDEO_AMP_BANDWIDTH)

    elif description == "Various Settings":
        command_description_box.delete("1.0", "end")
        command_description_box.insert(tk.END, command_description.VARIOUS_SETTINGS)

    elif description == "Oscillator Trimming":
        command_description_box.delete("1.0", "end")
        command_description_box.insert(tk.END, command_description.OSCILLATOR_TRIM)

    elif description == "Temperature Sensors":
        command_description_box.delete("1.0", "end")
        command_description_box.insert(tk.END, command_description.TEMP_SENSORS)

    elif description == "Analog Control Settings":
        command_description_box.delete("1.0", "end")
        command_description_box.insert(tk.END, command_description.ANALOG_CONTROL)

    elif description == "I2C Error Flag":
        command_description_box.delete("1.0", "end")
        command_description_box.insert(tk.END, command_description.I2C_ERROR_FLAG)

    elif description == "Chip Revision":
        command_description_box.delete("1.0", "end")
        command_description_box.insert(tk.END, command_description.CHIP_REVISION)

    elif description == "Software Reset":
        command_description_box.delete("1.0", "end")
        command_description_box.insert(tk.END, command_description.SOFTWARE_RESET)

    command_description_box.configure(state='disabled')


update_command_description_box(command_description_selected.get())

command_description_selected.bind('<<ComboboxSelected>>',
                                  lambda event: update_command_description_box(command_description_selected.get()))
########################################################################################################################

########################################################################################################################
# Serial Monitor Frame #################################################################################################
########################################################################################################################

# Send Command Entry Box ###############################################################################################
command_to_send = tk.StringVar()
send_command = tk.Entry(serial_monitor_frame,
                        textvariable=command_to_send,
                        bg="white",
                        justify="right",
                        width=20)

send_command.grid(column=0,
                  row=1,
                  padx=const.X_COLUMN_PAD,
                  pady=const.Y_OPTION_PAD,
                  stick='w')


########################################################################################################################

# Send Command Button ##################################################################################################
def send_command_click(port_open, new_command):
    if port_open:
        serial_com.send_string(new_command)
        # print(new_command)
        print_to_serial_monitor("Sent: " + new_command)
        send_command.delete("0", "end")
    else:
        print_to_serial_monitor("Port not open!")


send_command_button = tk.Button(serial_monitor_frame,
                                text="Send",
                                command=lambda: send_command_click(serial_com.port_open, command_to_send.get()),
                                font=BUTTON_LABEL_FONT,
                                bg="#008000",
                                fg="white",
                                height=1,
                                width=6)

send_command_button.grid(column=0,
                         row=1,
                         padx=const.X_COLUMN_PAD,
                         pady=const.Y_OPTION_PAD,
                         sticky='e')

main_window.bind('<Return>', lambda event: send_command_click(serial_com.port_open, command_to_send.get()))
main_window.bind('<KP_Enter>', lambda event: send_command_click(serial_com.port_open, command_to_send.get()))

########################################################################################################################

# Serial Monitor #######################################################################################################
serial_monitor_label = ttk.Label(serial_monitor_frame,
                                 text="Send Command:",
                                 font=OPTION_FONT)

serial_monitor_label.grid(column=0,
                          row=0,
                          padx=const.X_COLUMN_PAD,
                          pady=const.Y_OPTION_PAD,
                          stick='w')

serial_monitor = tk.Text(serial_monitor_frame,
                         height=16,
                         # width=40,
                         spacing2=5,
                         font=("Times New Roman", 9),
                         padx=const.X_COLUMN_PAD,
                         pady=const.Y_OPTION_PAD)

serial_monitor.grid(column=0,
                    row=2,
                    padx=const.X_COLUMN_PAD,
                    stick='ew')

serial_monitor_scrollbar = tk.Scrollbar(serial_monitor_frame,
                                        orient='vertical',
                                        command=serial_monitor.yview)

serial_monitor_scrollbar.grid(column=0,
                              row=2,
                              padx=const.X_COLUMN_PAD,
                              sticky='nse')
serial_monitor['yscrollcommand'] = serial_monitor_scrollbar.set


def print_to_serial_monitor(text):  # Print to Serial Monitor
    # Get time sinch the epoch and convert to datetime
    dt = datetime.fromtimestamp(t.time())
    # Format and convert to string
    time_stamp = dt.strftime("%H:%M:%S.%f")

    serial_monitor.insert(END, time_stamp + ":  " + text + '\n')
    if globe.SERIAL_MONITOR_AUTOSCROLL:
        serial_monitor.see(tk.END)


########################################################################################################################

# Serial Monitor Options ###############################################################################################
# Auto scroll
def toggle_sm_autoscroll(state):
    if state == 1:
        sm_autoscroll_checkbox.select()
        globe.SERIAL_MONITOR_AUTOSCROLL = True
    elif state == 0:
        sm_autoscroll_checkbox.deselect()
        globe.SERIAL_MONITOR_AUTOSCROLL = False


sm_autoscroll = tk.IntVar()
sm_autoscroll_checkbox = tk.Checkbutton(serial_monitor_options_frame,
                                        text="Autoscroll",
                                        variable=sm_autoscroll,
                                        onvalue=1,
                                        offvalue=0,
                                        command=lambda: toggle_sm_autoscroll(sm_autoscroll.get()))

sm_autoscroll_checkbox.grid(column=0,
                            row=0,
                            padx=const.X_COLUMN_PAD,
                            pady=const.Y_OPTION_PAD,
                            stick='w')

sm_autoscroll_checkbox.select()


# Show WAIT messages
def toggle_sm_show_wait(state):
    if state == 1:
        sm_show_wait_checkbox.select()
        globe.SERIAL_MONITOR_SHOW_WAIT = True
    elif state == 0:
        sm_show_wait_checkbox.deselect()
        globe.SERIAL_MONITOR_SHOW_WAIT = False


sm_show_wait = tk.IntVar()
sm_show_wait_checkbox = tk.Checkbutton(serial_monitor_options_frame,
                                       text="Show WAIT",
                                       variable=sm_show_wait,
                                       onvalue=1,
                                       offvalue=0,
                                       command=lambda: toggle_sm_show_wait(sm_show_wait.get()))

sm_show_wait_checkbox.grid(column=1,
                           row=0,
                           padx=const.X_COLUMN_PAD,
                           pady=const.Y_OPTION_PAD,
                           stick='w')

sm_show_wait_checkbox.deselect()


########################################################################################################################

# Clear Serial Monitor Button ##########################################################################################
def clear_serial_monitor_button_click():
    serial_monitor.delete("1.0", "end")


clear_serial_monitor_button = tk.Button(serial_monitor_options_frame,
                                        text="Clear Output",
                                        command=lambda: clear_serial_monitor_button_click(),
                                        font=BUTTON_LABEL_FONT,
                                        bg="black",
                                        fg="white",
                                        height=1,
                                        width=14)

clear_serial_monitor_button.grid(column=0,
                                 row=1,
                                 padx=const.X_COLUMN_PAD,
                                 pady=const.Y_OPTION_PAD,
                                 stick='e')


########################################################################################################################

# Serial Port Monitoring Thread ########################################################################################
def background_serial_port_monitor():
    while True:
        # Polling throttle needed to lighten CPU load
        t.sleep(0.1)

        if len(serial_com.serial_monitor_data_buffer) > 0:
            # Read next element in buffer. Buffer is FIFO so the next element
            # to read will always be at index zero until the buffer is empty.
            incoming_data = serial_com.serial_monitor_data_buffer[0]

            # Sort incoming data
            if "WAIT" in incoming_data:
                if globe.SERIAL_MONITOR_SHOW_WAIT is True:
                    print_to_serial_monitor(incoming_data)

            elif "D " in incoming_data:
                if globe.SERIAL_MONITOR_PRINT_DATA is True:
                    print_to_serial_monitor(incoming_data)

            elif "R " in incoming_data:
                print_to_serial_monitor(incoming_data)

            elif "BEGIN" or "$" in incoming_data:
                print_to_serial_monitor(incoming_data)

            # Remove processed element from buffer
            serial_com.serial_monitor_data_buffer.pop(0)


########################################################################################################################

########################################################################################################################
# Graphing Tab #########################################################################################################
########################################################################################################################

##################
# Plot variables #
##################

# Waterfall plot ######

# Line Plot ######
x = []
y = []
x_min = 0
x_max = 1023
y_min = 0
y_max = 1023


# Initial conditions generator #
def generate_initial_conditions():
    # Waterfall plot

    # Line plot
    i = 0
    while i <= 1023:
        x.append(i)
        y.append(512)
        i += 1


# Line Plot ############################################################################################################
generate_initial_conditions()

x_array = np.asarray(x)

# Generate Figure and Canvas to house the plot
fig = Figure(  # figsize=(4, 4),
    dpi=100)

# adding the subplot
rt_plot = fig.add_subplot(111)
rt_plot.set_xlim(x_min, x_max)
rt_plot.set_ylim(y_min, y_max)
scat = rt_plot.scatter(x, y, c='black', s=1)
rt_plot.set_title("ESPROS epc901 Real-Time Plotter", fontsize=10)
rt_plot.set_xlabel("X Direction", fontsize=6)
rt_plot.set_ylabel("ADC Counts", fontsize=6)

# creating the Tkinter canvas containing the Matplotlib figure
canvas = FigureCanvasTkAgg(fig,
                           master=plot_frame)
canvas.draw()

# placing the canvas on the Tkinter window
canvas.get_tk_widget().pack(fill=X)

# creating the Matplotlib toolbar
toolbar = NavigationToolbar2Tk(canvas,
                               plot_frame)
toolbar.update()

# placing the toolbar on the Tkinter window
canvas.get_tk_widget().pack()


def start_line_plot():
    ani = animation.FuncAnimation(fig,
                                  update_line_plot,
                                  interval=100,
                                  fargs=(x_array, scat)
                                  # blit=True
                                  )
    canvas.draw()


def update_line_plot(i, x_arr, scatter):
    if globe.LINE_PLOT_STATE == const.ACTIVE:
        if len(serial_com.line_plotter_data_buffer) > 0:
            line_arr = np.asarray(serial_com.line_plotter_data_buffer[0])
            line = np.column_stack((x_arr, line_arr))
            scatter.set_offsets(line)

            serial_com.line_plotter_data_buffer.pop(0)
            return scatter
            # return [scatter]  # Use with blit=true


########################################################################################################################

# Single Line Plot #####################################################################################################

########################################################################################################################

# Start Capture button #################################################################################################
def start_capture_button_click():
    if serial_com.port_open:
        serial_com.send_string(command.CONTINUOUS_CAPTURE)
        print_to_serial_monitor("Sent: " + command.CONTINUOUS_CAPTURE)
        start_capture_button.configure(bg="green")

        # Activate other buttons
        # pause_capture_button.configure(state='normal')
        stop_capture_button.configure(state='normal')
        clear_plots_button.configure(state='normal')

        # Declare the plots active
        globe.WATERFALL_PLOT_STATE = const.ACTIVE
        globe.LINE_PLOT_STATE = const.ACTIVE

        # Subsequent calls to start_line_plot() causes the animation to freeze
        if not globe.PLOTS_STARTED:
            start_line_plot()
            globe.PLOTS_STARTED = True


start_capture_button = tk.Button(plot_control_buttons_frame,
                                 text="Start",
                                 command=lambda: start_capture_button_click(),
                                 font=BUTTON_LABEL_FONT,
                                 bg="#326c88",
                                 fg="black",
                                 height=1,
                                 width=9)

start_capture_button.grid(column=0,
                          row=0,
                          padx=const.X_COLUMN_PAD,
                          pady=const.Y_BUTTON_PAD - 2,
                          stick='w')


########################################################################################################################

# Pause Capture button ################################################################################################
# def pause_capture_button_click():
#     if serial_com.port_open:
#         serial_com.send_string(command.STOP_CAPTURE)
#         print_to_serial_monitor("Sent: " + command.STOP_CAPTURE)
#         start_capture_button.configure(bg="#326c88")
#
#         # Declare plots idle
#         globe.WATERFALL_PLOT_STATE = const.IDLE
#         globe.LINE_PLOT_STATE = const.IDLE
#
#
# pause_capture_button = tk.Button(plot_control_buttons_frame,
#                                  text="Pause",
#                                  command=lambda: pause_capture_button_click(),
#                                  font=BUTTON_LABEL_FONT,
#                                  bg="#326c88",
#                                  fg="black",
#                                  height=1,
#                                  width=9)
#
# pause_capture_button.grid(column=0,
#                           row=1,
#                           padx=const.X_COLUMN_PAD,
#                           pady=const.Y_BUTTON_PAD - 2,
#                           stick='w')
#
# pause_capture_button.configure(state='disabled')


########################################################################################################################

# Stop Capture Button ##################################################################################################
def stop_capture_button_click():
    if serial_com.port_open:
        serial_com.send_string(command.STOP_CAPTURE)
        print_to_serial_monitor("Sent: " + command.STOP_CAPTURE)
        start_capture_button.configure(bg="#326c88")

        # De-active other buttons
        # pause_capture_button.configure(state='disabled')

        # Declare plots idle
        globe.WATERFALL_PLOT_STATE = const.IDLE
        globe.LINE_PLOT_STATE = const.IDLE


stop_capture_button = tk.Button(plot_control_buttons_frame,
                                text="Stop",
                                command=lambda: stop_capture_button_click(),
                                font=BUTTON_LABEL_FONT,
                                bg="#ba2121",
                                fg="black",
                                height=1,
                                width=9)

stop_capture_button.grid(column=0,
                         row=1,
                         padx=const.X_COLUMN_PAD,
                         pady=const.Y_BUTTON_PAD - 2,
                         stick='w')

stop_capture_button.configure(state='disabled')


########################################################################################################################

# Clear Plots Button ##################################################################################################
def clear_plots_button_click():
    generate_initial_conditions()


clear_plots_button = tk.Button(plot_control_buttons_frame,
                               text="Clear Graph",
                               command=lambda: clear_plots_button_click(),
                               font=BUTTON_LABEL_FONT,
                               bg="#ffeb3b",
                               fg="black",
                               height=1,
                               width=9)

clear_plots_button.grid(column=0,
                        row=3,
                        padx=const.X_COLUMN_PAD,
                        pady=const.Y_BUTTON_PAD - 2,
                        stick='w')

clear_plots_button.configure(state='disabled')


########################################################################################################################

########################################################################################################################
def onclosing():
    if serial_com.port_open:
        # Close out serial port and join thread(s)
        serial_com.close_serial_port()
        serial_com.join_thread()

        # Join Serial Monitor, monitor thread
        globe.BG_SERIAL_PORT_MONITOR_THREAD.join(0.5)

    main_window.destroy()


main_window.protocol("WM_DELETE_WINDOW", onclosing)
main_window.mainloop()
