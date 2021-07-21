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


doPlots = True

# create a buoy field
datum = (42.4, -171.3)
myAUV = AUV(latlon=(42.4, -171.3), heading=90, datum=datum)


### ################################
#Set up the buoy field
buoyField = BuoyField(datum,
                      position_style='P')

nGates = 10
buoy_field_config = {'nGates': nGates,
                     'gate_spacing': 100,
                     'gate_width': 10,
                     'max_offset': 30,
                     'style': 'linear',
                     'heading': 90}

buoyField.configure(buoy_field_config)
buoyField.show_field() # Plot the green and red buoys
#buoyField.scan_field(num_buoys=3)
##################################

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
while not done:
    myAUV.update_state(dt)
    current_position = myAUV.get_position()
        
    auv_track.append(current_position)
    buoyField.check_buoy_gates(auv_track[-2], auv_track[-1])
    gnext, rnext = buoyField.next_gate()
    if gnext is None:
        print(f"Congratulations you have cleared {nGates} gates in {running_time} seconds. You issued {num_commands} commands.")
        break
    
    # current heading of vehicle
    auv_state = myAUV.get_state()

    # ***YOUR CODE HERE. ***    
    command = auv_controller.decide(auv_state, gnext, rnext)
    
    if command is not None:
        reply = myAUV.helm_command(command)
        print(f"{reply}")
        num_commands += 1

    # ***YOUR CODE HERE***    
    tgt_hdg = auv_controller.get_desired_heading()
    
    print(f"auv_heading is {auv_state['heading']}, target heading is {tgt_hdg}")
        
    if doPlots and not (frame % frame_skip):
        plt.plot(gnext[0], gnext[1], 'go') # plot next green buoy
        plt.plot(rnext[0], rnext[1], 'ro') # plot next red buoy
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
    if buoyField.missed_gate(auv_track[-2], current_position):
        print(f"End of mission: you successfully cleared {buoyField.clearedBuoys()} gates of {nGates} in {running_time} seconds. You issued {num_commands} commands.")
        done = True    

