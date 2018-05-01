#!/usr/bin/env python
import rospy
from custom_msgs.msg import *
from custom_msgs.srv import *
from std_msgs.msg import String


class SectionIdentifier:

    def __init__(self):
        # In ROS, nodes are uniquely named. If two nodes with the same
        # node are launched, the previous one is kicked off. The
        # anonymous=True flag means that rospy will choose a unique
        # name for our 'listener' node so that multiple listeners can
        # run simultaneously.
        rospy.init_node('section_identifier', anonymous=True)
        self.isInSection = False

        self.pub = rospy.Publisher('section_identifier', String, queue_size=0)

        rospy.Subscriber("truck_state", TruckState, self.callback)
        # rospy.Subscriber("section_lock", String, self.release_callback)

    def callback(self, data):
        x = data.p.x
        y = data.p.y
        # 1# 600 < x < 1800 and 5600 < y < 7300     #  Intersection 1
        # 2# 600 < x < 1800 and 3200 < y < 4700     #  Intersection 2
        # 3# 1900 < x < 3800 and 2550 < y < 5400    #  Roundabout
        # 4# 2600 < x < 3800 and 5600 < y < 7400    #  Intersection 3

        if 600 < x < 1800 and 5600 < y < 7300:
            self.pub.publish("Intersection_1")
        elif 600 < x < 1800 and 3200 < y < 4700:
            self.pub.publish("Intersection_2")
        elif 1900 < x < 3850 and 2550 < y < 5500:
            self.pub.publish("Roundabout")
        elif 2600 < x < 3850 and 5600 < y < 7400:
            self.pub.publish("Intersection_3")

        if 600 < x < 3800 and 500 < y <= 2300:
            self.pub.publish("Left_Curve")locals()
        elif 600 < x < 3800 and 7500 <= y < 9500:
            self.pub.publish("Right_Curve")


if __name__ == '__main__':
    s = SectionIdentifier()
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

'''
        
    def release_callback(self, data):
        print("release_callback - out " + "Data: " + data.data)
        if data.data == "release":
            self.isInSection = False
            print("release_callback - in")        


        
'''