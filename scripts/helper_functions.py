from __future__ import division
import math


def getAngleBetweenPoints(p1, p2):
    if p2.x - p1.x != 0:
        # print ("atan((%d - %d)/(%d - %d)) = atan(%f)" % (p2.y,p1.y,p2.x,p1.x, float(p2.y - p1.y)/float(p2.x - p1.x)))
        # return math.atan(float(p2.y-p1.y)/float(p2.x-p1.x))
        # print ("atan2((%d - %d), (%d - %d))" % (p2.y, p1.y, p2.x, p1.x))
        return math.atan2(p2.y - p1.y, p2.x - p1.x)
    else:
        return 1337
        # Driving along the Y-axis gives diff_X = p2.x - p1.x = 0 which is undefined.
        # 1337 - value is used in getActionFromRadians() to identify forward-driving when driving from
        # left -> right || right -> left


def getActionFromRadians(beta, initialDir):
    if initialDir == 'left':

        if -(math.pi / 4) < beta <= math.pi / 4:
            return 'turn_right'
        elif -(math.pi) + math.pi / 4 < beta <= -(math.pi / 4) or 1337:
            return 'forward'
        else:
            return 'turn_left'

    if initialDir == 'right':
        if -(math.pi / 4) < beta <= math.pi / 4:
            return 'turn_left'
        elif -(math.pi + math.pi / 4) < beta <= -math.pi or math.pi - (math.pi / 4) < beta <= math.pi:
            return 'turn_right'
        else:
            return 'forward'

    if initialDir == 'up':

        if -(math.pi / 4) < beta <= math.pi / 4:
            return 'forward'
        elif -(math.pi) + math.pi / 4 < beta <= -(math.pi / 4):
            return 'turn_left'
        else:
            return 'turn_right'

    if initialDir == 'down':
        if -(math.pi) + math.pi / 4 < beta <= -(math.pi / 4):
            return 'turn_right'
        elif -(math.pi + math.pi / 4) < beta <= -math.pi or math.pi - (math.pi / 4) < beta <= math.pi:
            return 'forward'
        else:
            return 'turn_left'


def getDirection(p1, p2):
    dx = p2.x - p1.x
    dy = p2.y - p1.y

    beta = math.atan2(dy, dx)

    if -(math.pi / 4) < beta <= math.pi / 4:
        return 'up'
    elif -(math.pi) + math.pi / 4 < beta <= -(math.pi / 4):
        return 'left'
    elif -(math.pi + math.pi / 4) < beta <= -math.pi or math.pi - (math.pi / 4) < beta <= math.pi:
        return 'down'
    else:
        return 'right'
