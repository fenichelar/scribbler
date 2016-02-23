#!/usr/local/bin/python2

from myro import *

init("/dev/tty.scribbler")

def getDirection(direction):
    if direction is 'left':
        return 1
    elif direction is 'right':
        return -1
    else:
        raise NameError('Invalid direction!')

def obstableDetected():
    return (max(getObstacle()) > 1500)

def moveForward():
    translate(1)

def moveForwardUntilWall():
    moveForward()
    while not obstableDetected():
        pass
    stop()

def rotate90Degrees(direction):
    stop()
    rotate(direction)
    wait(.63)
    stop()

def checkForWall(direction):
    stop()
    rotate90Degrees(-direction)
    obstable = obstableDetected()
    rotate90Degrees(direction)
    return obstable


wallTurnDirection = getDirection('right')
moveForwardUntilWall()
rotate90Degrees(wallTurnDirection)
moveForward()
counter = 0
while not obstableDetected():
    counter+=1
    if counter > 10:
        if checkForWall(wallTurnDirection):
            moveForward()
            counter = 0
        else:
            break
stop()
