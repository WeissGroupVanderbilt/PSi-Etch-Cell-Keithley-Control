# =============================================================================
# Keithley Sourcemeter GUI for Porous Silicon Etching 
# This script uses the PyMeasure library to write commands to your sourcemeter
# Zachary Martin 
# Last Updated: 10/25/2024
# =============================================================================


import PySimpleGUI as sg
import time
import numpy as np
from pymeasure.instruments.keithley import Keithley2400
from pymeasure.adapters import VISAAdapter
#PyVisa handles communication to devices and can be used for serial, GPIB, and more 

# Using the Keithley class from PyMeasure along with example methods:
# =============================================================================
adapter = VISAAdapter("ASRL6::INSTR") #ASRL6 = COM6
keithley = Keithley2400(adapter)
# #keithley = Keithley2400("ASRL3::INSTR") #COM3
# 
# keithley.apply_current()                # Sets up to source current
# keithley.source_current_range = 3.15   # Sets the source current range to 3.15A
keithley.compliance_voltage = 21        # Sets the compliance voltage to 21 V
keithley.source_voltage_range = 21      #sets sourve voltage range up to 21V 
keithley.source_current = 0             # Sets the source current to 0 mA
# keithley.disable_source()                # disables the source output
# keithley.measure_voltage()              # Sets up to measure voltage

#keithley.ramp_to_current(5e-3)          # Ramps the current to 5 mA
#print(keithley.voltage)                 # Prints the voltage in Volts

#keithley.shutdown()                     # Ramps the current to 0 mA and disables output
# =============================================================================

# Setting up the GUI window that allows for the use to input etching time, iterations, current density, delay

layout = [  [sg.Text('Etching Step 1',justification='center')],
          [sg.Text('Current Density'), sg.InputText(key='curr1', default_text=0), sg.Text('Time'), sg.InputText(key='time1',default_text=0), sg.Text('# Iterations'), sg.InputText(key='loop1',default_text=0)],
            [sg.Text('Etching Step 2',justification='center')],
          [sg.Text('Current Density'), sg.InputText(key='curr2',default_text=0), sg.Text('Time'), sg.InputText(key='time2',default_text=0), sg.Text('# Iterations'), sg.InputText(key='loop2',default_text=0)],
            [sg.Text('Etching Step 3',justification='center')],
            [sg.Text('Current Density'), sg.InputText(key='curr3',default_text=0), sg.Text('Time'), sg.InputText(key='time3',default_text=0), sg.Text('# Iterations'), sg.InputText(key='loop3',default_text=0)],
              [sg.Text('Etching Step 4',justification='center')],
            [sg.Text('Current Density'), sg.InputText(key='curr4',default_text=0), sg.Text('Time'), sg.InputText(key='time4',default_text=0), sg.Text('# Iterations'), sg.InputText(key='loop4',default_text=0)],
            [sg.Text('Etching Step 5',justification='center')],
            [sg.Text('Current Density'), sg.InputText(key='curr5',default_text=0), sg.Text('Time'), sg.InputText(key='time5',default_text=0), sg.Text('# Iterations'), sg.InputText(key='loop5',default_text=0)],
              [sg.Text('Etching Step 6',justification='center')],
            [sg.Text('Current Density'), sg.InputText(key='curr6',default_text=0), sg.Text('Time'), sg.InputText(key='time6',default_text=0), sg.Text('# Iterations'), sg.InputText(key='loop6',default_text=0)],
            [sg.Text('Etching Step 7',justification='center')],
            [sg.Text('Current Density'), sg.InputText(key='curr7',default_text=0), sg.Text('Time'), sg.InputText(key='time7',default_text=0), sg.Text('# Iterations'), sg.InputText(key='loop7',default_text=0)],
              [sg.Text('Etching Step 8',justification='center')],
            [sg.Text('Current Density'), sg.InputText(key='curr8',default_text=0), sg.Text('Time'), sg.InputText(key='time8',default_text=0), sg.Text('# Iterations'), sg.InputText(key='loop8',default_text=0)],           
            [sg.InputText(default_text='Enter Delay Here',key='delay')],
              [sg.Button('Start'), sg.Button('Cancel')],
            
            ]

# Create the Window
window = sg.Window("Zack's Etching Extravaganza", layout)

# Event Loop to process events and get the values of the inputs from he user
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    if event == 'Start':
        
        delay_num = int(values['delay'])
        
        loop1_num = int(values['loop1'])
        time1_num = int(values['time1'])       
        curr1_num = int(values['curr1'])
        
        loop2_num = int(values['loop2'])
        time2_num = int(values['time2'])       
        curr2_num = int(values['curr2'])
        
        loop3_num = int(values['loop3'])
        time3_num = int(values['time3'])       
        curr3_num = int(values['curr3'])
        
        loop4_num = int(values['loop4'])
        time4_num = int(values['time4'])       
        curr4_num = int(values['curr4'])
        
        loop5_num = int(values['loop5'])
        time5_num = int(values['time5'])       
        curr5_num = int(values['curr5'])
        
        loop6_num = int(values['loop6'])
        time6_num = int(values['time6'])       
        curr6_num = int(values['curr6'])
        
        loop7_num = int(values['loop7'])
        time7_num = int(values['time7'])       
        curr7_num = int(values['curr7'])
        
        loop8_num = int(values['loop8'])
        time8_num = int(values['time8'])       
        curr8_num = int(values['curr8'])

        # Arrays of current, iterations, and etching times
        iteration_array = np.array([loop1_num,loop2_num,loop3_num,loop4_num,loop5_num,loop6_num,loop7_num,loop8_num])
        time_array = np.array([time1_num,time2_num,time3_num,time4_num,time5_num,time6_num,time7_num,time8_num])
        current_array = np.array([curr1_num,curr2_num,curr3_num,curr4_num,curr5_num,curr6_num,curr7_num,curr8_num])

        #Set up a progress bar that will record total time of etching
        t = 0
        
        #don't need to delay after last iteration- right now it will delay after the last etch
        
        #calculate the total time for etching
        maxTime = np.sum(iteration_array*time_array.reshape(1,8)) + np.sum(iteration_array)*delay_num

        
        #progress bar instantiation         
        if maxTime != 0: sg.one_line_progress_meter("Progress meter",t,int(maxTime))
        
        # Go through the 8 etching steps
        
        for i in range(8):
            iterations = iteration_array[i]
            etchTime = time_array[i]
            keithley_current = current_array[i]
            
            print(f'Starting step {i+1}')

            #for each etching step, go through all the iterations
            
            for j in range(iterations):
                print(f'Starting iteration {j+1}')
                
                elapsedTime = 0
                currentTime = 0
                initTime = time.perf_counter()
                
                
                #Etching here for specified amount of time, set current output of keithley
# =============================================================================
                keithley.source_current = keithley_current
                keithley.enable_source()                # Enables the source output
# =============================================================================

                # Check how long we've been etching at this iteration and current
                while elapsedTime <= etchTime:
                    
                    currentTime = time.perf_counter()
                    elapsedTime = int(currentTime - initTime)
                    
                #update progress meter
                t = t + etchTime
                sg.one_line_progress_meter("Progress meter",t,int(maxTime))
     
                print(f'Finished etching step {i+1} iteration {j+1}. Now delaying.')
                #delay here, done with a single iteration
                #shut off source meter
# =============================================================================
                keithley.disable_source()                # disables the source output
 
# =============================================================================
                elapsedTime = 0.
                currentTime = 0.
                initTime = time.perf_counter()
                
                #this will delay after last step as well....
                while elapsedTime <= delay_num:
     
                    currentTime = time.perf_counter()
                    elapsedTime = int(currentTime - initTime)
     
                #update progress meter
                t = t + delay_num
                sg.one_line_progress_meter("Progress meter",t,int(maxTime))
            
            print(f'Finished step {i+1}') 
              

# All done. Close GUI

window.close()
# =============================================================================
keithley.shutdown()                     # Ramps the current to 0 mA and disables output
# =============================================================================



