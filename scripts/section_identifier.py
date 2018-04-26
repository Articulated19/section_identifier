#!/usr/bin/env python
import rospy
from helper_functions import *
from std_msgs.msg import *
from custom_msgs.msg import *


class SectionIdentifier:

    def __init__(self):
        rospy.init_node('section_identifier', anonymous=True)
        self.isInSection = False

        self.pub = rospy.Publisher('section_identifier', V2I, queue_size=0)

        rospy.Subscriber("truck_state", TruckState, self.callback)
        rospy.Subscriber("rviz_path", Path, self.handleNewPath)
        # rospy.Subscriber("section_lock", String, self.release_callback)

        self.actions = {
            'intersection1': None,
            'intersection2': None,
            'intersection3': None,
            'roundabout': None,
        }

        self.msg = V2I()
        self.msg_old = None
        self.truck_state = None
        self.nodes_in_each_section = None
        self.gotPath = False

    def resetActions(self):
        self.actions = {
            "Intersection_1": None,
            "Intersection_2": None,
            "Intersection_3": None,
            "Roundabout": None
        }

    def handleNewPath(self, data):
        self.resetActions()
        path = data.path
        if (len(path)) > 0:
            self.nodes_in_each_section = self.divideIntoSections(path)
            self.gotPath = True
            # self.setActionAtSections(sections)

        # Takes a path and sort the points them according to which section they belong to

    @staticmethod
    def divideIntoSections(path):
        intersection1 = []
        intersection2 = []
        intersection3 = []
        roundabout = []

        # 1# 600 < x < 1800  and 5600 < y < 7300    #  Intersection 1
        # 2# 600 < x < 1800  and 3200 < y < 4800    #  Intersection 2
        # 3# 2000 < x < 3850 and 2300 < y < 5600    #  Roundabout
        # 4# 2600 < x < 3850 and 5600 < y < 7300    #  Intersection 3

        for p in path:
            if 600 < p.x < 1800 and 5600 < p.y < 7300:
                intersection1.append(p)
            elif 600 < p.x < 1800 and 3200 < p.y < 4800:
                intersection2.append(p)
            elif 2000 < p.x < 3850 and 2300 < p.y < 5600:
                roundabout.append(p)
            elif 2600 < p.x < 3850 and 5600 < p.y < 7300:
                intersection3.append(p)

        return {
            "Intersection_1": intersection1,
            "Intersection_2": intersection2,
            "Intersection_3": intersection3,
            "Roundabout": roundabout
        }

    def setActionAtSections(self, section, nodes_in_section):
        if section == "Left_Curve" or section == "Right_Curve": # No action needed at curves
            return 0

        section_path = nodes_in_section[section]

        if len(section_path) > 1:
            #print "Section_path length: " + str(len(section_path))
            path_angle = getAngleBetweenPoints(section_path[0], section_path[-1])
            self.msg.initial_direction = getDirection(self.truck_state.p, section_path[1])
            #print("path0: (" + str(section_path[0].x) + ", " + str(section_path[0].y) + ")")
            #print("path-1: (" + str(section_path[-1].x) + ", " + str(section_path[-1].y) + ")")
            #print("truckstate: (" + str(self.truck_state.p.x) + ", " + str(self.truck_state.p.y) + ")")
            print("Path_Angle : " + str(path_angle))
            # print self.msg.initial_direction
            # print "Initial direction = " + self.msg.initial_direction
            # Set action for each section in custom_msg
            setattr(self.msg.action, section, getActionFromRadians(path_angle, self.msg.initial_direction))

    def callback(self, data):
        self.truck_state = data

        x = data.p.x
        y = data.p.y

        if 600 < x < 1800 and 5600 < y < 7300:
            self.msg.intersection = "Intersection_1"
        elif 600 < x < 1800 and 2800 < y < 4800:
            self.msg.intersection = "Intersection_2"
        elif 2000 < x < 3850 and 2300 < y < 5600:
            self.msg.intersection = "Roundabout"
        elif 2600 < x < 3850 and 5600 < y < 7300:
            self.msg.intersection = "Intersection_3"

        if 600 < x < 3800 and 500 < y <= 2300:
            self.msg.intersection = "Left_Curve"
        elif 600 < x < 1800 and 7300 <= y < 9500:
            self.msg.intersection = "Right_Curve"

        if self.msg.intersection != "" and self.msg.intersection != self.msg_old and self.gotPath :
            self.setActionAtSections(self.msg.intersection, self.nodes_in_each_section)
            self.pub.publish(self.msg)
            print self.msg
            self.msg_old = self.msg.intersection


if __name__ == '__main__':
    s = SectionIdentifier()

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
