#!/usr/bin/env python
import rospy
from custom_msgs.msg import *
from std_msgs.msg import String
from helper_functions import *


class SectionIdentifier:

    def __init__(self):
        rospy.init_node('section_identifier', anonymous=True)
        self.isInSection = False

        self.pub = rospy.Publisher('section_identifier', String, queue_size=0)

        rospy.Subscriber("truck_state", TruckState, self.callback)
        rospy.Subscriber("path_append", Path, self.handleNewPath)
        # rospy.Subscriber("section_lock", String, self.release_callback)

        self.actions = {
            'intersection1': None,
            'intersection2': None,
            'intersection3': None,
            'roundabout': None,
        }

    def resetActions(self):
        self.actions = {
            'intersection1': None,
            'intersection2': None,
            'intersection3': None,
            'roundabout': None,
        }

    def handleNewPath(self, data):
        self.resetActions()
        path = data.path
        if (len(path)) > 0:
            sections = self.divideIntoSections(path)
            self.setActionAtSections(sections)


        # Takes a path and sort the points them according to which section they belong to
    def divideIntoSections(self, path):
        intersection1 = []
        intersection2 = []
        intersection3 = []
        roundabout = []

        for p in path:
            if 600 < p.x < 1800 and 5600 < p.y < 7300:
                intersection1.append(p)
            elif 600 < p.x < 1800 and 3200 < p.y < 4700:
                intersection2.append(p)
            elif 1900 < p.x < 3850 and 2550 < p.y < 5500:
                roundabout.append(p)
            elif 2600 < p.x < 3850 and 5600 < p.y < 7400:
                intersection3.append(p)

        return {
            "intersection1": intersection1,
            "intersection2": intersection2,
            "intersection3": intersection3,
            "roundabout": roundabout
        }

    def setActionAtSections(self, sections):
        for section_name in sections:

            section_path = sections[section_name]

            if len(section_path) > 1:
                pathAngle = getAngleBetweenPoints(section_path[0],section_path[-1])
                self.actions[section_name] = getActionFromRadians(pathAngle)

        print(self.actions)

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