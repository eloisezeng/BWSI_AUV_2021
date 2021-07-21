from math import atan2, pi
class AUVController(object):
    def __init__(self, auv_state={}): # not sure what will be auv_state default value
        self.auv_state = auv_state
        self.desired_heading = None
        """
        auv_state = {'heading': self.__heading,
                     'rudder': self.__rudder_position,
                     'speed': self.__speed_mps,        
                     'position': self.__position}
        """
    
    def decide(self, auv_state, gnext, rnext):  # Determine the helm command to pass to the AUV
        self.auv_state = auv_state
        xa, ya = self.auv_state['position']
        x = (gnext[0] + rnext[0]) / 2 # x coord of desired position
        y = (gnext[1] + rnext[1]) / 2 # y coord of desired position
        desired_position = (x, y) # midpoint of the gate
        self.desired_heading = atan2(x-xa, y-ya) * 180 / pi # Calculate desired heading
        desired_heading_to_hit_green = atan2(gnext[0] - xa, gnext[1] - ya) * 180 / pi # heading to hit green buoy
        desired_heading_to_hit_red = atan2(rnext[0] - xa, rnext[1] - ya) * 180 / pi # heading to hit red buoy
        buffer = 1.25
        if self.desired_heading < 0:
            self.desired_heading += 360
        if ((auv_state["heading"] < (desired_heading_to_hit_green - buffer)) and 
            (auv_state["heading"] > (desired_heading_to_hit_red + buffer))): # if AUV will pass through buoy
            command = "RUDDER AMIDSHIPS"
        elif (auv_state["heading"] - self.desired_heading) > 180:
            command = f"RIGHT FULL RUDDER"
        elif (self.desired_heading - auv_state["heading"]) > 180:
            command = f"LEFT FULL RUDDER"
        else:
            num_degrees = abs(auv_state["heading"] - self.desired_heading) # num degrees to turn
            rudder_position = num_degrees
            rudder_position = round(rudder_position)
            if auv_state["heading"] > self.desired_heading:
                if rudder_position <= 30:
                    command = f"LEFT {rudder_position} DEGREES RUDDER"
                else:
                    command = f"LEFT FULL RUDDER"
            elif auv_state["heading"] < self.desired_heading:
                if rudder_position <= 30:
                    command = f"RIGHT {rudder_position} DEGREES RUDDER"
                else:
                    command = f"RIGHT FULL RUDDER"
        return command
    
    def get_desired_heading(self):
        return self.desired_heading


	
		

