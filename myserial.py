import serial
import serial.tools.list_ports
import threading as tr
import time as t
import commands
import constants

command = commands.Commands()
const = constants.Constants()


class Serial:
    def __init__(self):
        # Class Variables
        self.raw_data = ""
        self.clean_data = ""
        self.serial_monitor_data_buffer = []
        self.line_plotter_data_buffer = []
        self.waterfall_data_buffer = []
        self.line_data_list = []
        self.read_port = False
        self.data_ready = False
        self.port_open = False
        self.begin = False
        self.thread = None
        self.avail_ports = []
        self.port_names = []
        self.serial_connection = None
        self.serial_time_out = False

        # Serial Config
        self.serial_port = ""
        self.baud_rate = ""
        self.timeout = 1  # Must specify timeout when using readline() (in seconds)
        self.write_timeout = 1
        self.bytesize = 8
        self.parity = 'N'
        self.stopbits = 1
        self.xonxoff = 0
        self.rtscts = 0
        #  self.flushInput() # Clear serial port input buffer

    def find_available_serial_ports(self):
        self.port_names.clear()
        self.avail_ports = serial.tools.list_ports.comports()  # Listen for and list available serial ports
        for i in range(len(self.avail_ports)):  # Iterate through available ports and extract the port name
            s = ' '.join(map(str, self.avail_ports[i]))  # Convert list item into a String
            p = s.partition(" ")[0]  # Remove the first element of String, i.e. the port name
            self.port_names.insert(i, p)  # Add element to new list of only port names
        return self.port_names

    def open_serial_port(self):
        print("Trying to open port " + self.serial_port + " at " + self.baud_rate + " baud")
        try:
            self.serial_connection = serial.Serial(self.serial_port, self.baud_rate)
        except:
            print("Failed to open port " + self.serial_port + " at " + self.baud_rate + " baud")
            self.close_serial_port()
        else:
            self.serial_connection.reset_input_buffer()
            print(self.serial_port + " opened at " + self.baud_rate + " baud")
            self.port_open = True
            self.reset_controller()

            # Clear data buffers
            self.serial_monitor_data_buffer.clear()
            self.line_plotter_data_buffer.clear()
            self.waterfall_data_buffer.clear()

            # Start port listening loop
            self.start_serial_read()

    def close_serial_port(self):
        self.read_port = False
        self.port_open = False
        self.begin = False

        self.serial_connection.close()
        print(self.serial_port + " closed.")

        # self.join_thread()

    def join_thread(self):
        self.thread.join(0.5)

    def send_string(self, com):
        com = com + "\n"
        self.serial_connection.write(bytes(com, 'utf-8'))

    def start_serial_read(self):
        if self.thread is None:
            self.thread = tr.Thread(target=self.background_read_thread)
            self.thread.start()

        self.read_port = True

    def background_read_thread(self):
        t.sleep(0.5)
        self.serial_connection.reset_input_buffer()
        while self.read_port:  # Poll serial port for data
            self.raw_data = self.serial_connection.readline().decode('utf-8')
            self.raw_data = self.raw_data.rstrip()  # Strip the terminating '\n' character

            # if there is new data, add it to export data buffer lists
            if len(self.raw_data) > 0:
                self.serial_monitor_data_buffer.append(self.raw_data)

                # Print everything to the console
                print(self.raw_data)

                # "BEGIN" message from controller means it just started/restarted
                if "BEGIN" in self.raw_data:
                    self.begin = True
                    # print(self.raw_data)

                # if "WAIT" in self.raw_data:
                # print(self.raw_data)

                if "D " in self.raw_data:  # Message contains data
                    # Remove data tag: "D "
                    self.clean_data = self.raw_data.partition("D ")[2]
                    # Remove commas and convert data to list
                    self.line_data_list = self.clean_data.split(",")
                    # Remove trailing empty space from list
                    self.line_data_list.remove('')
                    # Convert data from String to Int
                    self.line_data_list = [int(i) for i in self.line_data_list]
                    # Add new data to export data buffer
                    self.line_plotter_data_buffer.append(self.line_data_list)

                self.raw_data = ""

    def reset_controller(self):
        # Toggle DTR line to reset controller upon port opening
        self.serial_connection.dtr = True
        t.sleep(0.1)
        self.serial_connection.dtr = False
        self.serial_connection.dtr = True
