import math

def getAngleBetweenPoints(p1, p2):
    return math.atan2(p2.y - p1.y, p2.x - p1.x)

def getActionFromRadians(rads):
    if rads < 0:
        rads = rads + math.pi

    if 0 < rads <= math.pi / 3:
        return 'turn_right'
    elif math.pi / 3 < rads <= 2 * math.pi / 3:
        return 'forward'
    else:
        return 'turn_left'