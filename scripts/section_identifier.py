#!/usr/bin/env python
import rospy
from custom_msgs.msg import *
from custom_msgs.srv import *
from std_msgs.msg import String

pub = None

def callback(data):
    global pub
     # x > 600 || x 1500 
    # y > 5900 || y < 7000
    x = data.p.x
    y = data.p.y

    if x > 600 and x < 1500 and y > 5900 and y < 7000:
        pub.publish("STAPH THE TRUCK")

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('section_identifier', anonymous=True)

    global pub
    pub = rospy.Publisher('section_identifier', String, queue_size=10)

    rospy.Subscriber("truck_state", TruckState, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()