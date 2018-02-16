#!/usr/bin/env python
import rospy
from custom_msgs.msg import *
from custom_msgs.srv import *
from std_msgs.msg import String

class SectionIdentifier:
    def __init__(self):
        self.pub = rospy.Publisher('/section_identifier', String, queue_size=10)

        rospy.init_node('section_identifier', anonymous=True)
        rospy.Subscriber('truck_state', TruckState, self.truckStateHandler)
        
    def truckStateHandler(self, data):
         # x > 600 || x 1500 
        # y > 5900 || y < 7000

        self.pub.publish(data.p.x)
        self.pub.loginfo(data.p.y)

    def spin():
        rate = rospy.Rate(10) # 10hz
        while not rospy.is_shutdown():
            rate.sleep()

if __name__ == '__main__':
    s = SectionIdentifier()
    # s.spin()
