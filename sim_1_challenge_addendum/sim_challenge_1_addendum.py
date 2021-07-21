# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 20:49:23 2021

@author: JO20993
"""
from BWSI_AUV import AUV
from BWSI_BuoyField import BuoyField
from AUV_Controller import AUVController

import numpy as np
import matplotlib.pyplot as plt


doPlots = False

# create a buoy field
datum = (42.4, -171.3)


### ################################
#Set up the buoy field
buoyField = BuoyField(datum,
                      position_style='P')

nGates = 100
buoy_configs_all = list()
buoy_field_config = {'nGates': nGates,
                     'gate_spacing': 100,
                     'gate_width': 10,
                     'max_offset': 20,
                     'style': 'sine',
                     'sine_amplitude': 50,
                     'sine_period':500,
                     'heading': 50}
buoy_configs_all.append(buoy_field_config)

buoy_field_config = {'nGates': nGates,
                     'gate_spacing': 100,
                     'gate_width': 10,
                     'max_offset': 20,
                     'style': 'sine',
                     'sine_amplitude': 50,
                     'sine_period':500,
                     'heading': 177}
buoy_configs_all.append(buoy_field_config)

buoy_field_config = {'nGates': nGates,
                     'gate_spacing': 200,
                     'gate_width': 10,
                     'max_offset': 20,
                     'style': 'square',
                     'heading': 50}
buoy_configs_all.append(buoy_field_config)

buoy_field_config = {'nGates': nGates,
                     'gate_spacing': 200,
                     'gate_width': 10,
                     'max_offset': 20,
                     'style': 'square',
                     'heading': 0}
buoy_configs_all.append(buoy_field_config)

results = list()

for buoy_field_config in buoy_configs_all:
    myAUV = AUV(latlon=(42.4, -171.3), heading=buoy_field_config['heading']+22, datum=datum)


    buoyField.configure(buoy_field_config)
    # buoyField.show_field()
    #buoyField.scan_field(num_buoys=3)
    ##################################
    
    start_pos = myAUV.get_position()
    min_dist = buoyField.minimum_distance(start_pos)
    battery_init = 2*min_dist
    myAUV.set_battery(battery_init)
    
    #################################
    ## mission startup
    running_time = 0
    dt = 1
    cmd = "ENGINE HALF AHEAD"
    reply = myAUV.engine_command(cmd)
    print(f"{cmd} : {reply}")
    
    # keep the track history
    auv_track = list()
    auv_track.append(myAUV.get_position())
    
    if doPlots:
        fig = plt.figure()
        ax = fig.add_subplot(111)
    
    done = False
    
    auv_state = myAUV.get_state()
    
    # ***YOUR CODE HERE****
    auv_controller = AUVController(auv_state)
    
    num_commands = 0
    frame_skip = 10
    frame = 0
    current_time = 0
    while not done:
        current_time += dt
        myAUV.update_state(dt)
        battery_remain = myAUV.get_battery()
        current_position = myAUV.get_position()
        
        auv_track.append(current_position)
        buoyField.check_buoy_gates(auv_track[-2], auv_track[-1])
        gnext, rnext = buoyField.next_gate()
        if gnext is None:
            result_str = f"Congratulations you have arrived at your destination, clearing {nGates} gates in {running_time} seconds with {battery_remain/battery_init*100:.2f}% battery remaining. You issued {num_commands} commands."
            print(result_str)
            results.append(result_str)
            break
        
        # current heading of vehicle
        auv_state = myAUV.get_state()
    
        # ***YOUR CODE HERE***    
        command = auv_controller.decide(auv_state, gnext, rnext)
        
        if command is not None:
            reply = myAUV.helm_command(command)
            print(f"{reply}")
            num_commands += 1
    
        # ***YOUR CODE HERE***    
        tgt_hdg = auv_controller.get_desired_heading()
        #print(f"{gnext}, {rnext}, {current_position}")
        print(f"auv_heading is {auv_state['heading']}, target heading is {tgt_hdg}")
            
        if doPlots and not (frame % frame_skip):
            ax.clear()
            ax.plot(gnext[0], gnext[1], 'go')
            ax.plot(rnext[0], rnext[1], 'ro')
            trk = np.array(auv_track)
            ax.plot(trk[-300:,0], trk[-300:,1], 'k')            
    
            ax.set_xlim(current_position[0]-100, current_position[0]+100)
            ax.set_ylim(current_position[1]-100, current_position[1]+100)
            ax.set_aspect('equal')
    
            plt.pause(0.01)
            plt.draw()       
            
        frame += 1
    
        running_time = running_time + dt
        
        # are we done?
        if buoyField.missed_gate(auv_track[-2], current_position, current_time):
            result_str = f"End of mission (MISSED GATE): you successfully cleared {buoyField.clearedBuoys()} gates of {nGates} in {running_time} seconds. You issued {num_commands} commands."
            print(result_str)
            results.append(result_str)
            done = True
        if battery_remain <= 0:
            result_str = f"End of mission (OUT OF BATTERY): you successfully cleared {buoyField.clearedBuoys()} gates of {nGates} in {running_time} seconds. You issued {num_commands} commands."
            print(result_str)
            results.append(result_str)
            done = True


print('****** MISSION SUMMARY *********')            
for i, result in enumerate(results):
    print(f"MISSION {i}: {result}")    


