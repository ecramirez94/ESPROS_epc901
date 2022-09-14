# Project wide Variables

class Globals:
    def __init__(self):
        self.BG_SERIAL_PORT_MONITOR_THREAD = None

        # Serial Monitor Options
        self.SERIAL_MONITOR_AUTOSCROLL = True
        self.SERIAL_MONITOR_SHOW_WAIT = False
        self.SERIAL_MONITOR_PRINT_DATA = False

        # Plot Controls
        self.PLOTS_STARTED = False  # Needed to block the call to start_line_plot after subsequent starts
        self.LINE_PLOT_STATE = 0
        self.WATERFALL_PLOT_STATE = 0
