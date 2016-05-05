#!/usr/local/bin/python2

from myro import *
import numpy as np
import cv2
import csv

count = 0

init("/dev/tty.Fluke2-0D7B-Fluke2")

def detectBlobs(im):
    """ Takes and image and locates the potential location(s) of the red marker
        on top of the robot

    Hint: bgr is the standard color space for images in OpenCV, but other color
          spaces may yield better results

    Note: you are allowed to use OpenCV function calls here

    Returns:
      keypoints: the keypoints returned by the SimpleBlobDetector, each of these
                 keypoints has pt and size values that should be used as
                 measurements for the particle filter
    """

    #YOUR CODE HERE
    _,im = cv2.threshold(im[:,:,1], 140, 170, cv2.THRESH_BINARY)

    params = cv2.SimpleBlobDetector_Params()
    params.filterByArea = True
    params.minArea = 100
    params.maxArea = 10000000000
    params.filterByCircularity = False
    params.filterByColor = False
    params.filterByConvexity = False
    params.filterByInertia = False

    keypoints = cv2.SimpleBlobDetector(params).detect(im)
    return keypoints

def predict(particles, predictSigma):
    """ Predict particles one step forward. The motion model should be additive
        Gaussian noise with sigma predictSigma

    Returns:
      particles: list of predicted particles (same size as input particles)
    """

    #YOUR CODE HERE
    for p in particles:
        p[0] = np.random.normal(p[0], predictSigma)
        p[1] = np.random.normal(p[1], predictSigma)

    return particles

def update(particles, weights, keypoints):
    """ Resample particles and update weights accordingly after particle filter
        update

    Returns:
      newParticles: list of resampled partcles of type np.array
      weights: weights updated after sampling
    """

    #YOUR CODE HERE
    weights = []
    for particle in particles:
        arr = []
        for keypoint in keypoints:
            arr.append(np.linalg.norm(particle-np.asarray(keypoint.pt)))
        weights.append(1 / np.math.pow(min(arr), 3))

    weights = weights / np.sum(weights)
    return particles, weights

def resample(particles, weights):
    """ Resample particles and update weights accordingly after particle filter
        update

    Returns:
      newParticles: list of resampled partcles of type np.array
      wegiths: weights updated after sampling
    """

    #YOUR CODE HERE
    l = particles.shape[0]
    weights = weights / np.sum(weights)

    density = np.zeros(l)
    density[0] = weights[0]
    for i in range(1, l):
        density[i] = weights[i] + density[i - 1]

    for i in range(0, l):
        arr = np.asarray(density) - np.random.rand(1)[0]
        arr[arr < 0] = 1
        particles[i] = particles[arr.argmin()]
        weights[i] = weights[arr.argmin()]

    return particles, weights/np.sum(weights)

def obstableDetected():
    return (max(getObstacle()) > 1000)

def moveForwardUntilWall():
    global count
    count = 0
    translate(1)
    while not obstableDetected():
        pass
    stop()

def rotate45Degrees():
    global count
    count = count + 1
    if count > 10:
        moveForwardUntilWall()
    stop()
    rotate(1)
    wait(.3)
    stop()

def rotateXDegrees(x):
    global count
    count = 0
    stop()
    if x < 0:
        rotate(1)
    elif x > 0:
        rotate(-1)
    wait(.2*abs(x))
    stop()

def moveForward():
    global count
    count = 0
    stop()
    translate(1)
    wait(1)
    stop()

if __name__ == "__main__":
    global count
    imageWidth = 427
    imageHeight = 266
    numParticles = 1000
    initialScale = 50
    predictionSigma = 150
    picName = 'picture.jpg'
    setPicSize("small")
    autoCamera()

    while True:
        x = np.random.uniform(0, imageWidth, (numParticles, 1))
        y = np.random.uniform(0, imageHeight, (numParticles, 1))
        particles = np.concatenate((x,y), axis=1)
        weights = np.ones(numParticles)/numParticles

        if not obstableDetected():
            translate(.33)
        else:
            stop()

        pic = takePicture()
        im = cv2.cvtColor(np.array(pic.image), cv2.COLOR_RGB2BGR)
        yuv = cv2.cvtColor(im, cv2.COLOR_BGR2YUV)
        particles = predict(particles, predictionSigma)
        keypoints = detectBlobs(yuv)
        if keypoints:
            keypoint = cv2.KeyPoint()
            for point in keypoints:
                if point.size > keypoint.size:
                    keypoint = point
            particles, weights = update(particles, weights, keypoints)
            point = (int(keypoint.pt[0]), int(keypoint.pt[1]))
            size = int(np.ceil(keypoint.size/10))
            position = (float(point[0]-(imageWidth/2.0)))/float(imageWidth/2.0)

            #print 'Position: ' + str(position)
            #print 'Size: ' + str(size)
            #cv2.circle(im, point, radius=size, color=(255,0,0), thickness=size)
            #cv2.imwrite(picName, im)
            #cv2.imshow("Image", im)
            #cv2.waitKey()
            if obstableDetected():
                moveForward()
                rotate45Degrees()
                rotate45Degrees()
            elif point[1] > imageHeight*.75:
                rotate45Degrees()
            elif size < 3:
                rotate45Degrees()
            else:
                rotateXDegrees(position)
                moveForward()
        else:
            rotate45Degrees()
