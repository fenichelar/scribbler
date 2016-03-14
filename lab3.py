#!/usr/local/bin/python2

from myro import *
from mosaic import *

init("/dev/tty.scribbler")

def calculateAngle(angle):
    img_a = cv2.imread('00_degrees.png')[::2,::2,:]
    img_b = cv2.imread('%02d_degrees.png'%angle)[::2,::2,:]

    _, best_H = img_combine_homog(img_a, img_b, 1000, 600)
    K = cam_params_to_mat(CAM_KX, CAM_KY, CAM_CX, CAM_CY)
    y_ang = extract_y_angle(rot_from_homog(best_H, K))

    return np.rad2deg(y_ang)

def rotateAndCalculateAngle():
    angles = []
    savePicture(takePicture('gray'), '00_degrees.png')
    for angle in range(5,50,5):
        turnBy(5, 'deg')
        savePicture(takePicture('gray'), '%02d_degrees.png'%angle)
        angles.append(calculateAngle(angle))
    print angles

def calculateSet2Image():
    multi_pair_combine(1, 5)

rotateAndCalculateAngle()
