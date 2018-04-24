#!/usr/bin/env python
import rospy
from custom_msgs.msg import *
from std_msgs.msg import String
from helper_functions import *
from section import *
import math

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
    def divideIntoSections(self, path):
        intersection1 = []
        intersection2 = []
        intersection3 = []
        roundabout = []

        section_map = SectionIdentifier.getSectionMap()
        is1 = section_map["intersection1"]
        is2 = section_map["intersection2"]
        is3 = section_map["intersection3"]
        rbt = section_map["roundabout"]

        for p in path:
            if is1.min_x < p.x < is1.max_x and is1.min_y < p.y < is1.max_y:
                intersection1.append(p)
            elif is2.min_x < p.x < is2.max_x and is2.min_y < p.y < is2.max_y:
                intersection2.append(p)
            elif is3.min_x < p.x < is3.max_x and is3.min_y < p.y < is3.max_y:
                intersection3.append(p)
            elif rbt.min_x < p.x < rbt.max_x and rbt.min_y < p.y < rbt.max_y:
                roundabout.append(p)

        return {
            "intersection1": intersection1,
            "intersection2": intersection2,
            "intersection3": intersection3,
            "roundabout": roundabout
        }

    def setActionAtSections(self, sections):
        for section_name, section_path in sections.iteritems():

            if len(section_path) > 1:
                path_angle = getAngleBetweenPoints(section_path[0],section_path[-1])
                #print section_name + " angle: " + str(path_angle*180/math.pi)
                initial_dir = getDirection(section_path[0], section_path[1])
                self.actions[section_name] = getActionFromRadians(path_angle, initial_dir)

        print(self.actions)

    def callback(self, data):
        x = data.p.x
        y = data.p.y

        section_map = SectionIdentifier.getSectionMap()
        is1 = section_map["intersection1"]
        is2 = section_map["intersection2"]
        is3 = section_map["intersection3"]
        rbt = section_map["roundabout"]

        '''
        if is1.min_x < x < is1.max_x and is1.min_y < y < is1.max_y:
            self.pub.publish("Intersection_1")
        elif is2.min_x < x < is2.max_x and is2.min_y < y < is2.max_y:
            self.pub.publish("Intersection_2")
        elif is3.min_x < x < is3.max_x and is3.min_y < y < is3.max_y:
            self.pub.publish("Intersection_3")
        elif rbt.min_x < x < rbt.max_x and rbt.min_y < y < rbt.max_y:
            self.pub.publish("Roundabout")
        '''

    @staticmethod
    def getSectionMap():

        return {
            "intersection1": Section(600, 1800, 5600, 7300),
            "intersection2": Section(600, 1800, 3200, 4700),
            "intersection3": Section(2600, 3850, 5600, 7400),
            "roundabout": Section(1900, 3850, 2550, 5500),
        }


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