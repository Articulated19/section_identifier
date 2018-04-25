#!/usr/bin/env python
import rospy
from custom_msgs.msg import *
from std_msgs.msg import String
from helper_functions import *


class SectionClients:

    def __init__(self):
        rospy.init_node('section_clients', anonymous=True)
        self.isInSection = False

        self.pub = rospy.Publisher('section_clients', String, queue_size=0)

        rospy.Subscriber("section_identifier", String, self.release_callback)

    # def callback(self, data):


if __name__ == '__main__':
    s = SectionClients()
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
