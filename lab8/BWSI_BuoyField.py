# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 12:39:28 2021

@author: JO20993
"""

import sys
import time

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import utm

## Utility functions
def corridor_check(A, G, R):
    GR = np.array((R[0]-G[0], R[1]-G[1]))
    GA = np.array((A[0]-G[0], A[1]-G[1]))
    RA = np.array((A[0]-R[0], A[1]-R[1]))
    
    GRGA = np.dot(GR, GA)
    GRRA = np.dot(GR, RA)

    return (GRGA*GRRA < 0)

def gate_check(B, A, G, R):
    
    if not (corridor_check(A, G, R) and corridor_check(B, G, R) ):
        return False
    
    GR = np.array((R[0]-G[0], R[1]-G[1], 0))
    GA = np.array((A[0]-G[0], A[1]-G[1], 0))
    GB = np.array((B[0]-G[0], B[1]-G[1], 0))
    
    GRGA = np.cross(GR, GA)
    GRGB = np.cross(GR, GB)
    
    return (GRGA[2]*GRGB[2] < 0)

class Buoy(object):
    def __init__(self,
                 datum,
                 position=[],
                 latlon=[]):
                
        assert (latlon or position) and not (latlon and position), "Buoy.__init__: Must define either latlon or position!"

        self.__datum = datum
        # returns easting, northing, section #, section letter
        self.__datum_position = utm.from_latlon(self.__datum[0], self.__datum[1])
        
        
        if not latlon:
            self.__position = position
            
            # calculate its latlon
            self.__latlon = utm.to_latlon(self.__position[0] + self.__datum_position[0],
                                          self.__position[1] + self.__datum_position[1],
                                          self.__datum_position[2],
                                          self.__datum_position[3])

        else:
            self.__latlon = latlon
            position = utm.from_latlon(self.__latlon[0],
                                       self.__latlon[1],
                                       force_zone_number=self.__datum_position[2],
                                       force_zone_letter=self.__datum_position[3])
            self.__position = (position[0]-self.__datum_position[0],
                               position[1]-self.__datum_position[1])
                    
        
    def update_position(self, newpos):
        postn = (newpos[0], newpos[1], self.__position[2], self.__position[3])
        self.__position = postn
        self.__latlon = utm.to_latlon(self.__position[0] + self.__datum_position[0],
                                      self.__position[1] + self.__datum_position[1],
                                      self.__datum_position[2],
                                      self.__datum_position[3])
                 
    def update_latlon(self, newlatlon):
        self.__latlon = newlatlon
        self.__position = utm.from_latlon(self.__latlon[0],
                                          self.__latlon[1],
                                          force_zone_numer=self.__datum_position[2],
                                          force_zone_letter=self.__datum_position[3])
            
    # accessor functions
    def get_position(self):
        return self.__position
    
    def get_latlon(self):
        return self.__latlon
        

## Buoy field class
class BuoyField(object):
    def __init__(self,
                 datum,
                 green_buoys = [],
                 red_buoys = [],
                 position_style='P'):
        
        # position_style = 'P' for position, 'L' for latlon
        self.__datum = datum
        self.__datum_position = utm.from_latlon(self.__datum[0], self.__datum[1])

        self.add_buoy_gates(green_buoys, red_buoys, position_style)
        
    def configure(self, config):
        nGates = config['nGates']
        gate_spacing = config['gate_spacing']
        half_width = config['gate_width']/2.0
        
        if (config['style'].lower() == 'linear'):
            gate_max_offset = config['max_offset']
            random_samples = np.random.random((nGates, 1))
            green_buoy = list()
            red_buoy = list()
            for i in range(nGates):
                # space the gates by gate_spacing
                xdist = (i+1)*gate_spacing
                ydist = (random_samples[i][0] - 0.5) * gate_max_offset
                green_buoy.append((xdist,
                                   ydist + half_width))
                red_buoy.append((xdist,
                                 ydist - half_width))
                
            self.add_buoy_gates(green_buoy, red_buoy)

    
    def add_buoy_gates(self, green, red, position_style='P'):
        
        assert len(green) == len(red), "Should be equal number of green and red buoys"
        assert position_style=='P' or position_style=='L', f"Unknown position style {position_style}"
        self.__green_buoys = list()
        self.__red_buoys = list()
        for i in range(len(green)):
            if position_style == 'P':
                self.__green_buoys.append(Buoy(self.__datum, position=green[i]))
                self.__red_buoys.append(Buoy(self.__datum, position=red[i]))
            else:
                self.__green_buoys.append(Buoy(self.__datum, latlon=green[i]))
                self.__red_buoys.append(Buoy(self.__datum, latlon=red[i]))

        self.gates_passed = np.zeros( (len(red),), dtype=bool)
        
    def get_buoy_positions(self):
        G = list()
        R = list()
        for green in self.__green_buoys:
            G.append(green.get_position())
        for red in self.__red_buoys:
            R.append(red.get_position())
        return (G,R)
    
    def get_buoy_latlon(self):
        G = list()
        R = list()
        for green in self.__green_buoys:
            G.append(green.get_latlon())
        for red in self.__red_buoys:
            R.append(red.get_latlon())
        return (G,R)
        
        
    def check_buoy_gates(self, prev_pos, new_pos):
        
        for i in range(self.gates_passed.size):
            if (self.gates_passed[i] == False):
                self.gates_passed[i] = gate_check(new_pos, 
                                                  prev_pos, 
                                                  self.__green_buoys[i].get_position(),
                                                  self.__red_buoys[i].get_position())
                            
    def clearedBuoys(self):
        return np.count_nonzero(self.gates_passed)
    
    def isClear(self):
        return (np.count_nonzero(self.gates_passed) == self.gates_passed.size)
        
    # return all the buoys in the field that are within max_range of the platform,
    # and between angle_left and angle_right (in absolute bearing)
    def detectable_buoys(self,
                         position,
                         max_range,
                         angle_left,
                         angle_right,
                         sensor_type='POSITION'):
        # note: angle_left and angle_right are mod 360
        G = list()
        for green in self.green_buoys:
            rng = np.sqrt( (position[0]-green[0])**2 + (position[1]-green[1])**2 )
            if rng < max_range:
                # now check if it's within the angle range atan2 returns -pi:pi
                angl = np.mod(np.degrees(np.arctan2(green[0]-position[0], green[1]-position[1]) ), 360)
                if (angle_left < angle_right):
                    if ( angl >= angle_left and angl <= angle_right ):
                        if sensor_type == 'POSITION':
                            G.append(green)
                        elif sensor_type == 'RANGE_ANGLE':
                            G.append((rng, angl))
                        elif sensor_type == 'ANGLE':
                            G.append(angl)
                        elif sensor_type == 'RANGE':
                            G.append(rng)
                        else:
                            sys.exit()
                else:
                    if ( angl >= angle_left or angl <= angle_right):
                        if sensor_type == 'POSITION':
                            G.append(green)
                        elif sensor_type == 'RANGE_ANGLE':
                            G.append((rng, angl))
                        elif sensor_type == 'ANGLE':
                            G.append(angl)
                        elif sensor_type == 'RANGE':
                            G.append(rng)
                        else:
                            sys.exit()
                    
        R = list()
        for red in self.red_buoys:
            rng = np.sqrt( (position[0]-red[0])**2 + (position[1]-red[1])**2 )
            if rng < max_range:
                # now check if it's within the angle range atan2 returns -pi:pi
                angl = np.mod(np.degrees(np.arctan2(red[0]-position[0], red[1]-position[1]) ), 360)
                if (angle_left < angle_right):
                    if (angl >= angle_left and angl <= angle_right):
                        if sensor_type == 'POSITION':
                            R.append(red)
                        elif sensor_type == 'RANGE_ANGLE':
                            R.append((rng, angl))
                        elif sensor_type == 'ANGLE':
                            R.append(angl)
                        elif sensor_type == 'RANGE':
                            R.append(rng)
                        else:
                            sys.exit()
                else:
                    if (angl >= angle_left or angl <= angle_right):
                        if sensor_type == 'POSITION':
                            R.append(red)
                        elif sensor_type == 'RANGE_ANGLE':
                            R.append((rng, angl))
                        elif sensor_type == 'ANGLE':
                            R.append(angl)
                        elif sensor_type == 'RANGE':
                            R.append(rng)
                        else:
                            sys.exit()
        
        return G, R
        
    def show_field(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        for i in range(len(self.__green_buoys)):
            Gpos = self.__green_buoys[i].get_position()
            plt.plot( Gpos[0], Gpos[1], 'go')
            Rpos = self.__red_buoys[i].get_position()
            plt.plot( Rpos[0], Rpos[1], 'ro')
            
        glist, rlist = self.get_buoy_positions()
        garray = np.array(glist)
        rarray = np.array(rlist)
            
        plt.plot(garray[:,0], garray[:,1], 'g')
        plt.plot(rarray[:,0], rarray[:,1], 'r')

        #ax.set_aspect('equal')
        plt.show()
        
    def scan_field(self, num_buoys=3):
        # note: in Spyder, you must run %matplotlib qt in the console before using this!
        #scan the field num_buoys at a time
        fig = plt.figure()
        ax = fig.add_subplot(111)
        nGates = len(self.__green_buoys)

        glist, rlist = self.get_buoy_positions()
        garray = np.array(glist)
        rarray = np.array(rlist)

        plt.plot(garray[:,0], garray[:,1], 'go--')
        plt.plot(rarray[:,0], rarray[:,1], 'ro--')
        
        for i in range(nGates-num_buoys):
            minx = np.min(np.concatenate((garray[i:(i+num_buoys),0], rarray[i:(i+num_buoys),0])))
            maxx = np.max(np.concatenate((garray[i:(i+num_buoys),0], rarray[i:(i+num_buoys),0])))
            miny = np.min(np.concatenate((garray[i:(i+num_buoys),1], rarray[i:(i+num_buoys),1])))
            maxy = np.max(np.concatenate((garray[i:(i+num_buoys),1], rarray[i:(i+num_buoys),1])))
            ax.set_xlim(minx-100, maxx+100)
            ax.set_ylim(miny-100, maxy+100)
            ax.set_title('Buoy Corridor Preview')
            ax.set_aspect('equal')
            plt.draw()
            plt.pause(.25)
        
    # return the position of the next uncleared gate
    def next_gate(self):
        
        for i in range(self.gates_passed.size):
            if (self.gates_passed[i] == False):
                return self.__green_buoys[i].get_position(), self.__red_buoys[i].get_position()
        
        # if they're all passed
        return None, None
    
    # determine whether the vehicle has missed the next gate
    def missed_gate(self, prev_pos, cur_pos):
        gnext, rnext = self.next_gate()
        if gnext is None:
            return False
        
        gate_ctr = ((gnext[0]+rnext[0])/2.0, (gnext[1]+rnext[1])/2.0)
        prev_range = np.sqrt((prev_pos[0]-gate_ctr[0])**2 + (prev_pos[1]-gate_ctr[1])**2)
        cur_range = np.sqrt((cur_pos[0]-gate_ctr[0])**2 + (cur_pos[1]-gate_ctr[1])**2)
        
        print(f"cur_range = {cur_range}")
        
        return cur_range > prev_range

    ## return if all the gates are cleared        
    def all_gates_cleared(self):
        if all(self.gates_passed == True):
            return True
        else:
            return False