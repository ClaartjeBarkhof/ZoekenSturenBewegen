# ZSB - Opdracht 2             #
# errorreport.py               #
# 16/06/2017                   #
#                              #
# Anna Stalknecht - 10792872   #
# Claartje Barkhof - 11035129  #
# Group C                      #
#                              #
################################

'''
error report
We started implementing the board_position_to_cartesian function. This function was
tested by printing the cartesian values to see if thehy matched our calculation.
We also printed the board_position and the value of index function to see if it was working
correctly.

Then we implemented the high_path function which we tested by running the program and
pressing compute high path. We then checked the joints_simulation.txt file and saw that
something had changed. We couldn't really test it more because we first had to implement 
the inverse_kinematics.

So we made the inverse_kinematics function. And now we had te possibility to test it by
running the program. At first the program wasn't working properly because it took chesspieces
from the table instead of from the chessboard. We found out that it was because we switched x
and z axes. 

Then we tried rotating the chessboard and we found out that our board_position_to_cartesian wasn't
working properly. It was only working when we turned the chessboard 0 or 180 degrees. That was because 
we walked from h8 in the right angle but it didn't work the way we want. Than we changed
the function so it would calculate the cartesian from the original angle (0 degrees), and than 
calculationg that position to the new position at the right angle. Then it worked.

We then had an error rotationg the chessboard -20degrees, the shoulder_angle gave a math error.
That was because the arms are not big enough to reach the top of the board at that angle.
When placed the board closer to the gripper our program worked properly again.


'''