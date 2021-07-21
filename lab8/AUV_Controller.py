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
        desired_heading_to_hit_green = atan2(x-gnext[0], y-gnext[1]) # heading to hit green buoy
        desired_heading_to_hit_red = atan2(x-rnext[0], y-rnext[0]) # heading to hit red buoy
        if ((auv_state["heading"] > desired_heading_to_hit_green) and 
            (auv_state["heading"] < desired_heading_to_hit_red)): # if AUV will pass through buoy
            command = "RUDDER AMIDSHIPS"
        elif auv_state["heading"] > self.desired_heading:
            command = "LEFT STANDARD RUDDER"
        elif auv_state["heading"] < self.desired_heading:
            command = "RIGHT STANDARD RUDDER"
        return command
    
    def get_desired_heading(self):
        return self.desired_heading


	
		

