# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 20:49:23 2021

@author: BWSI AUV Challenge Instructional Staff
"""
from BWSI_AUV import AUV
from BWSI_BuoyField import BuoyField
from AUV_Controller import AUVController

import numpy as np
import matplotlib.pyplot as plt

COURSE_NUMBER=0
VISIBILITY=99

def select_buoy_field(course_num):
    ### ################################
    #Set up the buoy field
    nGates = 100
    
    if course_num==0:
        nGates = 50
        buoy_field_config = {'nGates': nGates,
                             'gate_spacing': 100,
                             'gate_width': 10,
                             'max_offset': 50,
                             'style': 'linear',
                             'heading': 52.3}

    elif course_num==1:
        buoy_field_config = {'nGates': nGates,
                             'gate_spacing': 100,
                             'gate_width': 10,
                             'max_offset': 20,
                             'style': 'sine',
                             'sine_amplitude': 50,
                             'sine_period':500,
                             'heading': 50}
    elif course_num==2: 
        buoy_field_config = {'nGates': nGates,
                             'gate_spacing': 100,
                             'gate_width': 10,
                             'max_offset': 20,
                             'style': 'sine',
                             'sine_amplitude': 50,
                             'sine_period':500,
                             'heading': 177}
    elif course_num==3:
        buoy_field_config = {'nGates': nGates,
                             'gate_spacing': 100,
                             'gate_width': 10,
                             'max_offset': 20,
                             'style': 'square',
                             'heading': 50}
    elif course_num==4:
        buoy_field_config = {'nGates': nGates,
                             'gate_spacing': 100,
                             'gate_width': 10,
                             'max_offset': 20,
                             'style': 'square',
                             'heading': 0}
    else:
        buoy_field_config = None

    return buoy_field_config

def main():
    doPlots = True
    
    # create a buoy field
    datum = (42.4, -171.3)
    
    # set up the buoy field
    buoyField = BuoyField(datum,
                          position_style='P')
    
        
    buoy_field_config = select_buoy_field(COURSE_NUMBER)
    buoyField.configure(buoy_field_config)
    buoyField.show_field()

    myAUV = AUV(latlon=(42.4, -171.3), heading=buoy_field_config['heading']+22, datum=datum, visibility=VISIBILITY)
    
    #buoyField.scan_field(num_buoys=3)
    ##################################
    
    start_pos = myAUV.get_position()
    min_dist = buoyField.minimum_distance(start_pos)
    battery_init = 10*min_dist
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
    frame_skip = 2
    frame = 0
    current_time = 0
    while not done:
        current_time += dt
        myAUV.update_state(dt)
        battery_remain = myAUV.get_battery()
        current_position = myAUV.get_position()
        
        auv_track.append(current_position)
        buoyField.check_buoy_gates(auv_track[-2], auv_track[-1])
        gsense, rsense = myAUV.read_laser(buoyField)
        gnext, rnext = buoyField.next_gate()
        if gnext is None:
            result_str = f"Congratulations you have arrived at your destination, clearing {buoy_field_config['nGates']} gates in {running_time} seconds with {battery_remain/battery_init*100:.2f}% battery remaining. You issued {num_commands} commands."
            print(result_str)
            break
        
        # current heading of vehicle
        auv_state = myAUV.get_state()
    
        # ***YOUR CODE HERE***    
        command = auv_controller.decide(auv_state, gsense, rsense, sensor_type='RANGE_ANGLE')
        
        if command is not None:
            reply = myAUV.helm_command(command)
            print(f"{reply}")
            num_commands += 1
    
        # ***YOUR CODE HERE***    
        tgt_hdg = auv_controller.get_desired_heading()
        #print(f"{gnext}, {rnext}, {current_position}")
        print(f"auv_heading is {auv_state['heading']}, target heading is {tgt_hdg}")
            
        if doPlots and not (frame % frame_skip):
            plt.plot(gnext[0], gnext[1], 'go')
            plt.plot(rnext[0], rnext[1], 'ro')
            trk = np.array(auv_track)
            plt.plot(trk[-300:,0], trk[-300:,1], 'k')            
    
            ax.set_xlim(current_position[0]-100, current_position[0]+100)
            ax.set_ylim(current_position[1]-100, current_position[1]+100)
            ax.set_aspect('equal')
    
            plt.pause(0.01)
            plt.draw()       
            
        frame += 1
    
        running_time = running_time + dt
        
        # are we done?
        if buoyField.missed_gate(auv_track[-2], current_position, current_time):
            result_str = f"End of mission (MISSED GATE): you successfully cleared {buoyField.clearedBuoys()} gates of {buoy_field_config['nGates']} in {running_time} seconds. You issued {num_commands} commands."
            print(result_str)
            done = True
        if battery_remain <= 0:
            result_str = f"End of mission (OUT OF BATTERY): you successfully cleared {buoyField.clearedBuoys()} gates of {buoy_field_config['nGates']} in {running_time} seconds. You issued {num_commands} commands."
            print(result_str)
            done = True
                
if __name__ == "__main__":
    main()    
    
