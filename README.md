# RoboDK postprocessor for Arctos 0.16.7

This repository contains RoboDK packages for the Arctos robotic arm, enabling motion planning, execution, and simulation in both virtual and real environments.
 
## How to Use:

### Requirements 

1. [RoboDK](https://robodk.com/download)
2. [UGS](https://winder.github.io/ugs_website/download/)

### Import Arctos.rdk in RoboDK 

1. File > Open > Arctos.rdk
2. Double click on Prog1 to see the test move 
3.  Import Arctos.py post processor to installation folder. 
    For example "C:\RoboDK\Posts"
4. Right click on Prog1 > Select Post Processor > there should be "Arctos" in the list. 
  
 ![Arctos_RoboDK.jpg](/Arctos_RoboDK.jpg)

### Generate robot program 

1. Right click on Prog1 > Generate robot program > select Arctos > OK 

If you want to make your custom program follow the RoboDK [tutorials](https://www.youtube.com/watch?v=xZ2_JEbS_E0&list=PLjiA6TvRACQd8pL0EnE9Djc_SCH7wxxXl)

In short: 
- double click on Arctos in design tree below the My Mechanism Base opens the panel
- In panel it is possible to jog and move the robot to desired position 
More fun way is to click anywhere in space and hit ALT key, it allows to move the robot 
by pivoting tools on each target. 
- Add target to desired position
- Create New program
- Select target
- Add movement to a program (joint, linear, circular) 
- Double click on Prog2 to see the movement
- Step 1.

  
### Open robot program in UGS 

1. Connect the robot with USB cable
2. Refresh the Port and select COM port, Select Baud 115200
3. Connect the robot
4. Make sure it is in the same position as target "Home" in RoboDK
5. File > Open > Prog1.gcode
6. Toolbox > Reset Zero
7. Play the program on robot 


## To do: 

1. Add gripper in RoboDK 
2. Custom macro in UGS for manual opening and closing the gripper 


