class CommandDescriptions:
    def __init__(self):
        self.BINNING = '''
        HOR_BIN: Horizontal binning of the pixels:
                 00: Binning 2 pixels (in differential mode only, n/a in single ended mode)
                 01: No binning (default)
                 10: Binning 4 pixels
                 
        Example Usage, set binning to 4 pixels: "HOR_BIN:10"
        '''

        self.AMPLIFIER_GAIN = '''
        GAIN: Video amplifier voltage gain:
              00: 2
              01: 1 (default)
              10: 4
        
        Example Usage, set video amplifier gain to 1: "GAIN:01"
        '''

        self.ROI = '''
        ROI_SEL: Region of Interest:
            0: All pixels (0 to 1023) (Default)
            1: Inner half of the pixels (256 to 767)
            
        Example Usage, set ROI to all pixels: "ROI_SEL:0"
        '''

        self.READ_DIRECTION = '''
        RD_DIR: Read direction:
            0: From 0 to 1023 (default)
            1: From 1023 to 0
            
        Example Usage, set read direction from 1023 to 0: "RD_DIR:1"
        '''

        self.VIDEO_AMP_BANDWIDTH = '''
        BW_VIDEO_1/0: Video Amplifier Bandwidth:
            1010: 1 MHz
            1000: 4 MHz
            0010: 8 MHz
            0101: 16 MHz (default)
            
        Example Usage, set BW to 4MHz: "BW_VIDEO:1000"
        
        ---------------------------------------------------------------------------------------
        
        VIDEO_GBW_SEL_REG: Video Amplifier Bandwidth, noise and current consumption.
            Code | Rel. Video Amp BW | Rel. Video Amp current consumption | Relative Read Noise
            ----------------------------------------------------------------------------------- 
            00    |      25%         |              Lowest                |       Lowest
            01    |       50%         |                                    |       
            10    |       75%         |                                      |       
            11    |       100%        |              Highest               |       Highest

        Example Usage, set relative BW + noise/current to 75%: "VIDEO_GBW:10"
        '''

        self.VARIOUS_SETTINGS = '''
        MISC_CONF: Configuration Control, Video Amplifier On/Off
            Video amplifier power-down: 
                1 = Off | 0 = On (Default)
                
            Example Usage, turn video amp off: "VIDEO_AMP_PD_OVR:1"
            
            -----------------------------------------------------------------------
            
            Configuration Control:
                1 = By configuration registers | 0 = By configuration pins (default)
            
            Example Usage, use configuration registers: "RD_CONF_CTRL:1"
        '''

        self.OSCILLATOR_TRIM = '''
        OSC_TRIM:
        
            Coarse Trimming:
                0 = Default oscillator trim range (default)
                1 = Oscillator frequency increased by 25%
            
            Example Usage, increase oscillator frequency by 25%: "OSC_TRIM_COARSE:1"
            
            ------------------------------------------------------------------------------
            
            Fine Trimming (in MHz):
                0: 0.0
                1: +1.2
                2: +2.4
                3: +3.6
                4: +4.8
                5: +6.0
                6: +7.2
                7: +8.4
                8: -9.6
                9: -8.4
                10: -7.2
                11: -6.0
                12: -4.8
                13: -3.6
                14: -2.4
                15: -1.2
                
            Example usage, set oscillator trim to +8.4 MHz: "OSC_TRIM:7" 
                
        '''

        self.TEMP_SENSORS = '''
        TEMP_SENS_CONF: Configure and measure relative temperature sensors.
            
            Measurement Rate:
                00: 10 Hz (default)
                01: 1 Hz
                10: 0.1 Hz
            
            Example Usage, set measurement rate to 1 Hz: "MEAS_RATE_CONF:01" 
            
            ------------------------------------------------------------------------------------
            
            Measure left temperature sensor (next to pixel 0; read-only):
                
                Example Usage: "TEMP_SENSE_L"
            
            ------------------------------------------------------------------------------------
            
            Measure right temperature sensor (next to pixel 1023; read-only):
            
                Example Usage: "TEMP_SENSE_R"
        '''

        self.ANALOG_CONTROL = '''
        FORCE_ANA_CTRL_SIGS:
            Video amplifier mode selection:
                0 = Single-ended (default)
                1 = Differential
                
            Example usage, set video amp mode to differential: "AMP_OVR:1"
            
            ------------------------------------------------------------------------------------
            
            Power control of the 5V regulator:
                0 = On (default)
                1 = Off
                
            Example usage, turn 5V regulator off: "VDD5V0_PD:1"
            
            ------------------------------------------------------------------------------------
            
            Power control of the charge pump:
                0 = On (default)
                1 = Off
                
            Example usage, turn charge pump off: "CP_PD:1"
        '''

        self.I2C_ERROR_FLAG = '''
        I2C_ERR (read-only): Bit set if I2C controller fails to service a register operation.
        
            Example Usage: "I2C_ERR"
        '''

        self.CHIP_REVISION = '''
        CHIP_REV_NO_REG (read-only): Chip revision number.
        
            Example Usage: "CHIP_REV_NO"
        '''

        self.SOFTWARE_RESET = '''
        Reset epc901 via software command. Has same effect as removing and re-applying power.
        
            Example Usage: "EPC_RESET"
        '''