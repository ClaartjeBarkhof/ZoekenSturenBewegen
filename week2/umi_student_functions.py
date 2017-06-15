#!python2

from __future__ import division, print_function
from umi_parameters import UMI_parameters
from umi_common import *
import math
import numpy as np
from visual import *
# Specifications of UMI
# Enter the correct details in the corresponding file (umi_parameters.py).
# <<<<<<<<<<-------------------------------------------------------------------- TODO FOR STUDENTS
UMI = UMI_parameters()

################################
# ZSB - Opdracht 2             #
# umi_student_functions.py     #
# 16/06/2017                   #
#                              #
# Anna Stalknecht - 10792872   #
# Claartje Barkhof - 11035129  #
# Group C                      #
#                              #
################################

'''
This file contains functions for the support of the UMI robot.
We implemented 3 functions: apply_inverse_kinematics, board_position_to_cartesian,
high_path and move_to_garbage. We implemented them making use of de slides of Leo Dorst on Robotics.
'''

def apply_inverse_kinematics(x, y, z, gripper):
    ''' Computes the angles of the joints, given some real world coordinates
        making use of inverse kinematics based on the Robotics readers made by
        Leo Dorst.
        :param float x: cartesian x-coordinate
        :param float y: cartesian y-coordinate
        :param float z: cartesian z-coordinate
        :return: Returns the a tuple containing the position and angles of the robot-arm joints.
    '''

    # Riser_position
    riser_position = y + UMI.total_arm_height

    # Variables:
    x_ik = x                        # x in inverse kinematics (x_ik)
    x_ik_2 = (x**2)                 # square of x_ik
    y_ik = z                        # z in inverse kinematics
    y_ik_2 = (z**2)                 # square of z_ik
    l_1 = UMI.upper_length          
    l_2 = UMI.lower_length
    l_1_2 = (UMI.upper_length**2)
    l_2_2 = (UMI.lower_length**2)

    # IK formulas
    elbow_angle = math.acos((x_ik_2 + y_ik_2 - l_1_2 - l_2_2)/(2*l_1*l_2))
    s_2 = (math.sqrt(1-(math.cos(elbow_angle)**2)))
    shoulder_angle = math.atan2(y_ik,x_ik) - atan2((l_2*s_2),(l_1+(l_2*math.cos(elbow_angle))))

    # Resulting angles in degrees
    elbow_angle = degrees(elbow_angle)
    shoulder_angle = degrees(shoulder_angle)

    # Resulting wrist angle (counter-turning the two other joints)
    wrist_angle = (-elbow_angle-shoulder_angle)

    return (riser_position, shoulder_angle, elbow_angle, wrist_angle, gripper)

def board_position_to_cartesian(chessboard, position):
    ''' Convert a position between [a1-h8] to its cartesian coordinates in frameworld coordinates.
        You are not allowed to use the functions such as: frame_to_world.
        You have to show actual calculations using positions/vectors and angles.
        :param obj chessboard: The instantiation of the chessboard that you wish to use.
        :param str position: A position in the range [a1-h8]
        :return: tuple Return a position in the format (x,y,z)
        def rotate(origin, point, angle):
    '''
    # Special garbage location
    if(position == 'j5'):
        row = -2
        column = 3
    # Normal locations (center of fields on the board)
    else:
        half_pi = (math.pi/2)
        letter = position[0]
        number = int(position[1])
        angle = -(chessboard.get_angle_radians())

        # Get the local coordinates for the tiles on the board in the 0-7 range.
        letter_list = ['h', 'g', 'f', 'e', 'd', 'c', 'b', 'a']
        number_list = [8,7,6,5,4,3,2,1]
        field_size = chessboard.field_size #meters
        (ox, oy, oz) = chessboard.get_position() # origin of rotation

        # Abstract column and row from the notation-form position
        column = letter_list.index(letter)
        row = number_list.index(number)

        # Calculate dz and dx measured from H8, the origin of rotation
        dz = (column+0.5) * field_size
        dx = (row+0.5) * field_size
        
        # Calculate dz and dx measured from H8, the origin of rotation
        pz = oz + dz
        px = ox + dx
        
        # The actual rotating point
        world_coordinate_z = oz + math.cos(angle) * (pz - oz) - math.sin(angle) * (px - ox)
        world_coordinate_x = ox + math.sin(angle) * (pz - oz) + math.cos(angle) * (px - ox)

    # y is not affected by the rotation
    world_coordinate_y = chessboard.get_board_height()

    # Output the results.
    result = (world_coordinate_x, world_coordinate_y, world_coordinate_z)
    return result

def high_path(chessboard, from_pos, to_pos):
    '''
    Computes the high path that the arm can take to move a piece from one place on the board to another.
    :param chessboard: Chessboard object
    :param from_pos: [a1-h8]
    :param to_pos: [a1-h8]
    :return: Returns a list of instructions for the GUI.
    '''
    sequence_list = []
    # We assume that 20 centimeter above the board is safe.
    safe_height = 0.2
    # We assume that 10 centimeter above the board is "low".
    low_height = 0.1

    # Get the coordinates.
    (from_x,from_y,from_z) = board_position_to_cartesian(chessboard, from_pos)
    (to_x,to_y,to_z) = board_position_to_cartesian(chessboard, to_pos)

    # Define half_piece_height according to which piece you are encountering (material)
    [nonsense, material, colour] = chessboard.pieces[from_pos]
    half_piece_height = (chessboard.pieces_height[material]/2)+chessboard.get_board_height()

    # Hover above the first field on SAFE height:
    sequence_list.append(apply_inverse_kinematics(from_x, safe_height, from_z, chessboard.field_size))

    # Hover above the first field on LOW height:
    sequence_list.append(apply_inverse_kinematics(from_x, low_height, from_z, chessboard.field_size))

    # Hover above the first field on half of the piece height:
    sequence_list.append(apply_inverse_kinematics(from_x, half_piece_height, from_z, chessboard.field_size))

    # Grip the piece
    sequence_list.append(apply_inverse_kinematics(from_x, half_piece_height, from_z, 0))

    # Give instruction to GUI to pickup piece
    sequence_list.append(["GUI", "TAKE", from_pos])

    # Hover above the first field on SAFE height, keeping the gripper closed
    sequence_list.append(apply_inverse_kinematics(from_x, safe_height, from_z, 0))

    # Move to new position on SAFE height
    sequence_list.append(apply_inverse_kinematics(to_x, safe_height, to_z, 0))

    # Hover above the second field on LOW height:
    sequence_list.append(apply_inverse_kinematics(to_x, low_height, to_z, 0))

    # Hover above the second field on half of the piece height:
    sequence_list.append(apply_inverse_kinematics(to_x, half_piece_height, to_z, chessboard.field_size))

    # Give instruction to GUI to drop piece
    sequence_list.append(["GUI", "DROP", to_pos])

    # Move to new position on SAFE height (And open the gripper)
    sequence_list.append(apply_inverse_kinematics(to_x, safe_height, to_z, chessboard.field_size))

    return sequence_list

def move_to_garbage(chessboard, from_pos):
    '''
        Computes the high path that the arm can take to move a piece from one place on the board to the garbage location.
        :param chessboard: Chessboard object
        :param from_pos: [a1-h8]
        :return: Returns a list of instructions for the GUI.
    '''
    sequence_list = []

    # We assume that 20 centimeter above the board is safe.
    safe_height = 0.2

    # We assume that 10 centimeter above the board is "low".
    low_height = 0.1

    drop_location = "j5"

    # Define half_piece_height according to which piece you are encountering (material)
    half_piece_height = (chessboard.pieces_height[material]/2)+chessboard.get_board_height()

    # Get the coordinates.
    (from_x, from_y, from_z) = board_position_to_cartesian(chessboard, from_pos)
    (to_x, to_y, to_z) = board_position_to_cartesian(chessboard, drop_location)

    # Hover above the first field on SAFE height:
    sequence_list.append(apply_inverse_kinematics(from_x, safe_height, from_z, chessboard.field_size))

    # Hover above the first field on LOW height:
    sequence_list.append(apply_inverse_kinematics(from_x, low_height, from_z, chessboard.field_size))

    # Hover above the first field on half of the piece height:
    sequence_list.append(apply_inverse_kinematics(from_x, half_piece_height, from_z, chessboard.field_size))

    # Grip the piece
    sequence_list.append(apply_inverse_kinematics(from_x, half_piece_height, from_z, 0))

    # Give instruction to GUI to pickup piece
    sequence_list.append(["GUI", "TAKE", from_pos])
    
    # Hover above the first field on SAFE height (Keep the gripper closed!!):
    sequence_list.append(apply_inverse_kinematics(from_x, safe_height, from_z, 0))

    # Move to new position on SAFE height
    sequence_list.append(apply_inverse_kinematics(to_x, safe_height, to_z, 0))

    # Hover above the second field on LOW height:
    sequence_list.append(apply_inverse_kinematics(to_x, low_height, to_z, 0))

    # Hover above the second field on half of the piece height:
    sequence_list.append(apply_inverse_kinematics(to_x, half_piece_height, to_z, chessboard.field_size))

    # Give instruction to GUI to drop piece
    sequence_list.append(["GUI", "DROP", drop_location])

    # Move to new position on SAFE height (And open the gripper)
    sequence_list.append(apply_inverse_kinematics(to_x, safe_height, to_z, chessboard.field_size))

    return sequence_list