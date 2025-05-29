# Simple code for temperature measurement using NI-9211 thermocouple module.
# -----------------------------------------
# Author: Gabriel Madeira
# Date: 2025-05-28
# -----------------------------------------
# This code requires the nidaqmx library. Install it using pip install nidaqmx.
# Make sure your Operating System is compatible with the NI-DAQmx driver required by the hardware.
# [important] Win 11 requires NIDAQmx 2022 Q3 for running NI-9211.
# -----------------------------------------

import nidaqmx as ni

with ni.Task() as task:
    task.ai_channels.add_ai_thrmcpl_chan("cDAQ1Mod2/ai3",                                   # Find this channel in Measurement & Automation Explorer (MAX)
                                         units=ni.constants.TemperatureUnits.DEG_C,        
                                         thermocouple_type=ni.constants.ThermocoupleType.K, 
                                         cjc_source=ni.constants.CJCSource.BUILT_IN)
    """ ADD THIS LINE FOR SIMULTANEOUS CONVERSION
    task.ai_channels.add_ai_thrmcpl_chan("cDAQ1Mod2/ai0",                                   
                                         units=ni.constants.TemperatureUnits.DEG_C,        
                                         thermocouple_type=ni.constants.ThermocoupleType.K, 
                                         cjc_source=ni.constants.CJCSource.BUILT_IN)
    """
    task.timing.cfg_samp_clk_timing(rate=25,                                               # Adjustable Sampling rate in Hz  
                                     active_edge=ni.constants.Edge.RISING,                  
                                     sample_mode=ni.constants.AcquisitionType.CONTINUOUS)   # Continuous sampling mode based on sample rate and samples per channel
    
    task.in_stream.input_buf_size = 10000 # Adjustable input buffer size, might need increase in long runs

    task.start()

    while True:
        temperature = task.read(number_of_samples_per_channel=5)     # Read 5 samples from the Aquistion Task (adjustable) and saves on an array
        print(f"Temperature: {temperature[0]} ºC")                   # Print a sample (OR first array in case of two sensoring) of the temperature reading
# The code above will run indefinitely, reading and printing 5 times per second.