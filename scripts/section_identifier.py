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
        rospy.Subscriber("rviz_path", Path, self.handleNewPath)
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

    @staticmethod
    def divideIntoSections(path):
        intersection1 = []
        intersection2 = []
        intersection3 = []
        roundabout = []

        # 1# 600 < x < 1800 and 5600 < y < 7300     #  Intersection 1
        # 2# 600 < x < 1800 and 3200 < y < 4800    #  Intersection 2
        # 3# 2000 < x < 3850 and 2550 < y < 5600    #  Roundabout
        # 4# 2600 < x < 3850 and 5600 < y < 7300    #  Intersection 3

        for p in path:
            if 600 < p.x < 1800 and 5600 < p.y < 7300:
                intersection1.append(p)
            elif 600 < p.x < 1800 and 3200 < p.y < 4800:
                intersection2.append(p)
            elif 2000 < p.x < 3850 and 2550 < p.y < 5600:
                roundabout.append(p)
            elif 2600 < p.x < 3850 and 5600 < p.y < 7300:
                intersection3.append(p)

        return {
            "intersection1": intersection1,
            "intersection2": intersection2,
            "intersection3": intersection3,
            "roundabout": roundabout
        }

    def setActionAtSections(self, sections):
        for section_name, section_path in sections.iteritems():

            if len(section_path) > 1:
                path_angle = getAngleBetweenPoints(section_path[0], section_path[-1])
                initial_dir = getDirection(section_path[0], section_path[1])
                self.actions[section_name] = getActionFromRadians(path_angle, initial_dir)

        print(self.actions)

    def callback(self, data):
        x = data.p.x
        y = data.p.y

        if 600 < x < 1800 and 5600 < y < 7300:
            self.pub.publish("Intersection_1")
        elif 600 < x < 1800 and 3200 < y < 4800:
            self.pub.publish("Intersection_2")
        elif 2000 < x < 3850 and 2550 < y < 5600:
            self.pub.publish("Roundabout")
        elif 2600 < x < 3850 and 5600 < y < 7300:
            self.pub.publish("Intersection_3")


if __name__ == '__main__':
    s = SectionIdentifier()
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

