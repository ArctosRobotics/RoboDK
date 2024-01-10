# Import RoboDK tools
from robodk import *

def pose_2_str(pose):
    """Prints a pose target"""
    [x, y, z, r, p, w] = pose_2_xyzrpw(pose)
    return ('X%.3f Y%.3f Z%.3f R%.3f P%.3f W%.3f' % (x, y, z, r, p, w))

def joints_2_str(joints):
    """Prints a joint target"""
    str = ''
    data = ['X ', ' Y', ' Z ', ' A ', ' B ', ' C ', 'F', 'H', 'I', 'J', 'K', 'L']
    for i in range(len(joints)):
        if i == 4:
            str = str + ('%s%.2f' % (data[i], -1 * joints[i]))  # flip joint 4 rotation
        else:
            str = str + ('%s%.2f' % (data[i], joints[i]))
    return str

# Object class that handles the robot instructions/syntax
class RobotPost(object):
    """Robot post object"""
    PROG_EXT = 'gcode'  # set the program extension

    # other variables
    ROBOT_POST = ''
    ROBOT_NAME = ''
    PROG_FILES = []

    PROG = ''
    LOG = ''
    nAxes = 6

    def __init__(self, robotpost=None, robotname=None, robot_axes=6, **kwargs):
        self.ROBOT_POST = robotpost
        self.ROBOT_NAME = robotname
        self.PROG = ''
        self.LOG = ''
        self.nAxes = robot_axes

    def ProgStart(self, progname):
        self.addline('F800 (Feedrate)')

    def ProgFinish(self, progname):
        self.addline('G90 X 0 Y 0 Z 0 A 0 B 0 C 0')

    def ProgSave(self, folder, progname, ask_user=False, show_result=False):
        progname = progname + '.' + self.PROG_EXT
        if ask_user or not DirExists(folder):
            filesave = getSaveFile(folder, progname, 'Save program as...')
            if filesave is not None:
                filesave = filesave.name
            else:
                return
        else:
            filesave = folder + '/' + progname
        fid = open(filesave, "w")
        fid.write(self.PROG)
        fid.close()
        print('SAVED: %s\n' % filesave)
        # ---------------------- show result
        if show_result:
            if type(show_result) is str:
                # Open file with provided application
                import subprocess
                p = subprocess.Popen([show_result, filesave])
            else:
                # open file with default application
                import os
                os.startfile(filesave)

            if len(self.LOG) > 0:
                mbox('Program generation LOG:\n\n' + self.LOG)

    def ProgSendRobot(self, robot_ip, remote_path, ftp_user, ftp_pass):
        ser = serial.Serial(COM10, baudrate=115200, timeout=10)

    def MoveJ(self, pose, joints, conf_RLF=None):
        """Add a joint movement"""
        self.addline('G90 ' + joints_2_str(joints))

    def MoveL(self, pose, joints, conf_RLF=None):
        """Add a linear movement"""
        self.addline('G90 ' + joints_2_str(joints))

    def MoveC(self, pose1, joints1, pose2, joints2, conf_RLF_1=None, conf_RLF_2=None):
        """Add a circular movement"""
        self.addline('G90 ' + joints_2_str(joints1))
        self.addline('G90 ' + joints_2_str(joints2))

    def setFrame(self, pose, frame_id=None, frame_name=None):
        """Change the robot reference frame"""

    def setTool(self, pose, tool_id=None, tool_name=None):
        """Change the robot TCP"""

    def Pause(self, time_ms):
        """Pause the robot program"""
        if time_ms < 0:
            self.addline('PAUSE')
        else:
            self.addline('M30T%s' % (time_ms))

    def setSpeed(self, speed_mms):
        """Changes the robot speed (in mm/s)"""

    def setAcceleration(self, accel_mmss):
        """Changes the robot acceleration (in mm/s2)"""

    def setSpeedJoints(self, speed_degs):
        """Changes the robot joint speed (in deg/s)"""
        self.SPEED_RADS = speed_degs * pi / 180
        self.addline('M105 %.3f' % self.SPEED_RADS)

    def setAccelerationJoints(self, accel_degss):
        """Changes the robot joint acceleration (in deg/s2)"""
        self.ACCEL_RADSS = accel_degss * pi / 180
        self.addline('M110 %i' % accel_degss)

    def setZoneData(self, zone_mm):
        """Changes the rounding radius (aka CNT, APO or zone data) to make the movement smoother"""

    def setDO(self, io_var, io_value):
        """Sets a variable (digital output) to a given value"""
        if type(io_var) != str:
            io_var = 'OUT[%s]' % str(io_var)
        if type(io_value) != str:
            if io_value > 0:
                io_value = 'TRUE'
            else:
                io_value = 'FALSE'

        self.addline('%s=%s' % (io_var, io_value))

    def waitDI(self, io_var, io_value, timeout_ms=-1):
        """Waits for a variable (digital input) io_var to attain a given value io_value. Optionally, a timeout can be provided."""
        if type(io_var) != str:
            io_var = 'IN[%s]' % str(io_var)
        if type(io_value) != str:
            if io_value > 0:
                io_value = 'TRUE'
            else:
                io_value = 'FALSE'

        if timeout_ms < 0:
            self.addline('WAIT FOR %s==%s' % (io_var, io_value))
        else:
            self.addline('WAIT FOR %s==%s TIMEOUT=%.1f' % (io_var, io_value, timeout_ms))

    def RunCode(self, code, is_function_call=False):
        """Adds code or a function call"""
        if is_function_call:
            code = code.replace(' ', '_')
            if not code.endswith('()'):
                code = code + '()'
            if code == 'Open()':
                self.addline('M97 G4P1 B40 T1')  # Add the G-code instructions for the Open subprogram
            elif code == 'Close()':
                self.addline('M97 G4P1 B0 T1')  # Add the G-code instructions for the Close subprogram
            else:
                self.addline(code)
        else:
            self.addline(code)

    def RunMessage(self, message, iscomment=False):
        """Display a message in the robot controller screen (teach pendant)"""
        if iscomment:
            if message == "Attach to Gripper V2":
                self.addline("M21")
            elif message == "Detach from Gripper V2":
                self.addline("M20")
        else:
            self.addlog('Show message on teach pendant not implemented (%s)' % message)

    def addlineEnd(self, newline):
        """Add a program line"""
        self.PROG = self.PROG + newline

    def addline(self, newline):
        """Add a program line"""
        self.PROG = self.PROG + newline + '\n'

    def addlog(self, newline):
        """Add a log message"""
        self.LOG = self.LOG + newline + '\n'
