import math

def getAngleBetweenPoints(p1, p2):
    if p2.x - p1.x != 0:
        return math.atan((p2.y-p1.y)/(p2.x-p1.x))
        #return math.atan2(p2.y-p1.y, p2.x - p1.x)
    else:
        print "ehrmagerd same x"
    return 0

def getActionFromRadians(rads):
    if rads <= -math.pi/4:
        return 'turn_left'
    elif -(math.pi/4) < rads < math.pi/4:
        return 'forward'
    elif rads >= math.pi/4:
        return 'turn_right'
