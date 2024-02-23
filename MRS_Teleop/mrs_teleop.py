#!/usr/bin/env python2


import rospy
from geometry_msgs.msg import Twist
import sys, select, os
if os.name == 'nt':
  import msvcrt
else:
  import tty, termios

msg = """
Communications Failed
"""


# Function responsible for using data taken from other robot, interpreting it, and using it to publish to personal diagnostics
def updater(data):
  
    # Data comes in difficult to read, make a string and split into a list
    data_list = str(data).split()

    # OS check to confirm settings
    if os.name != 'nt':
        settings = termios.tcgetattr(sys.stdin)

    # Initialize a publisher that will publish on the topic cmd_vel and will communicate with ROS Diagnostics
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)

    # Set the linear and angular velocities to their necessary values from the data_list variable
    target_linear_vel   = float(data_list[2])
    target_angular_vel  = float(data_list[-1])

    # Try this first, unless error, print "Communications Failed"
    try:
        # Initialize the message to be published
        twist = Twist()

        # Set the linear x to the value of target_linear_vel and the rest to 0 as the linear x is the only value taken into account from the robot motors
        twist.linear.x = target_linear_vel; twist.linear.y = 0.0; twist.linear.z = 0.0

        # Set the angular z to the value of target_angular_vel and the rest to 0 as the angular z is the only value taken into account from the robot motors
        twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = target_angular_vel

        # Publish the angular and linear velocities to the cmd_vel topic
        pub.publish(twist)

    except:
        print(msg)

    if os.name != 'nt':
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)


# Callback function called for subscriber. Logs caller ID and calls the updater function
def callback(data):

    # Log the caller ID and calls the updater function with the data gathered from the subscriber
    rospy.loginfo(rospy.get_caller_id())
    updater(data)


if __name__=="__main__":

    # Initialize Node Named Teleop Listener
    rospy.init_node('teleop_listener')

    # Initialize a subsciber that is listening to the cmd_vel topic on the leader and save the Twist information as a variable "data"
    data = rospy.Subscriber('/tb3_0/cmd_vel', Twist, callback)

    rospy.spin()
