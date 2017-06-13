#!python2

from __future__ import division, print_function

class UMI_parameters:
    def __init__(self):
        # Specifications of UMI
        # Zed
        self.hpedestal = 1.082 # di van riser/zed / 1000
        self.pedestal_offset = 0.0675 # ai van riser/zed / 1000
        self.wpedestal = 0.1 # just leave it 0.1

        # Dimensions upper arm
        self.upper_length = 0.2535 # ???? in meters (som van pythagoras van (ai + di), vd riser/zed-shoulder + shoulder-elbow)
        self.upper_height = 0.095 # ???? in meters (som van d1 + d2, oftewel z-verschuiving, vd riser/zed + shoulder)

        # Dimensions lower arm
        self.lower_length = 0.2535 # ???? in meters (som van pythagoras van (ai + di), vd elbow-wrist + wrist-gripper)
        self.lower_height = 0.080 # ???? in meters (som d3+d4)

        # Dimensions wrist
        self.wrist_height = 0.09 # ???? in meters

        # Height of the arm from the very top of the riser, to the tip of the gripper.
        self.total_arm_height = self.pedestal_offset + self.upper_height \
                                + self.lower_height + self.wrist_height

        # Joint-ranges in meters (where applicable e.g. Riser, Gripper) and in degrees for the rest.

        ## TODO for students: REPLACE MINIMUM_DEGREES AND MAXIMUM_DEGREES FOR EACH INDIVIDUAL JOINT, THEY ARE NOT THE SAME FOR
        # SHOULDER, ELBOW, AND WRIST
        self.joint_ranges = {
            "Riser"     : [0.0, 0.925],
            "Shoulder"  : [-90.0, 90.0],
            "Elbow"     : [110.0, 180.0],
            "Wrist"     : [-110.0, 110.0],
            "Gripper"   : [0, 0.05]
        }

    def correct_height(self, y):
        '''
            Function that corrects the y value of the umi-rtx, because the real arm runs from
            from -self.hpedestal/2 to self.hpedestal/2, while y runs from 0 to self.hpedestal.
        '''
        return y - 0.5*self.hpedestal
