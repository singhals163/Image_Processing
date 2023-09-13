import cv2
import numpy as np
import math

def buildFlag():
    array = np.zeros([600, 600, 3], dtype = np.uint8)
    # Green [ 0 128 0 ]
    # Orange [ 51 153 255]
    # Blue 245,   0,   0
    center = (299, 299)
    # center1 = (299, 300)
    # center2 = (300, 299)
    # center3 = (299, 299)
    # center4 = (301, 301)
    radius = 100
    color = (255, 0, 0)
    array[0:200, :] = [51, 153, 255]
    array[399:600, :] = [0, 128, 0]
    array[200:399, :] = [255, 255, 255]
    array = cv2.circle(array, center, radius, color, 1)
    # array = cv2.circle(array, center, radius-1, color, 1)
    # array = cv2.circle(array, center, 1, color, 2)
    # array = cv2.circle(array, center1, radius, color, 1)
    # array = cv2.circle(array, center2, radius, color, 1)
    # array = cv2.circle(array, center3, radius, color, 1)
    # array = cv2.circle(array, center4, radius, color, 1)
    num_lines = 24
    angle_increment = 15
    # Fixed length of the lines
    line_length = 99
    angle_degrees = 0
    # Draw the lines with fixed center, fixed length, and fixed angles
    for i in range(num_lines):
        angle_radians = math.radians(angle_degrees)
        # Calculate endpoint coordinates
        end_x = int(center[0] + line_length * math.cos(angle_radians))
        end_y = int(center[1] + line_length * math.sin(angle_radians))
        # print(end_x, end_y)
        # Draw the line
        color = (255, 0, 0)  # BGR color (red in this case)
        thickness = 1
        array = cv2.line(array, center, (end_x, end_y), color, thickness)
        angle_degrees += angle_increment

    return array

def sol(image):
    array = buildFlag()
    col = np.shape(image)[1]
    row = np.shape(image)[0]
    orange_left = False
    orange_top = False
    orange_right = False
    orange_bottom = False
    green_left = False
    green_top = False
    green_right = False
    green_bottom = False
    for i in range(row) :
        # print(i)
        if ((image[i][10] == np.array([51, 153, 255])).all()) :
            orange_left = True
        if ((image[i][10] == np.array([0, 128, 0])).all()) :
            green_left = True
        if ((image[i][col-11] == np.array([51, 153, 255])).all()) :
            orange_right = True
        if ((image[i][col-11] == np.array([0, 128, 0])).all()) :
            green_right = True
    for i in range(col) :
        if ((image[10][i] == np.array([51, 153, 255])).all()) :
            orange_top = True
        if ((image[10][i] == np.array([0, 128, 0])).all()) :
            green_top = True
        if ((image[row-11][i] == np.array([51, 153, 255])).all()) :
            orange_bottom = True
        if ((image[row-11][i] == np.array([0, 128, 0])).all()) :
            green_bottom = True
    
    if(orange_top and green_bottom):
        if((not orange_bottom) and (not green_top)):
            array = array

    if(orange_bottom and green_top):
        if((not orange_top) and (not green_bottom)):
            array = cv2.rotate(array, cv2.ROTATE_180)

    if(orange_left and green_right):
        if((not orange_right) and (not green_left)):
            array = cv2.rotate(array, cv2.ROTATE_90_COUNTERCLOCKWISE)

    if(orange_right and green_left):
        if((not orange_left) and (not green_right)):
            array = cv2.rotate(array, cv2.ROTATE_90_CLOCKWISE)
    # cv2.imshow("final", array)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # n = len(image_path)
    # cv2.imwrite('result'+ image_path[n-5] + '.png', array)
    return array


# Usage
def solution(image_path):
    image= cv2.imread(image_path)
    ######################################################################
    ######################################################################
    #####  WRITE YOUR CODE BELOW THIS LINE ###############################
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (h, w) = np.shape(gray_image)
    _, thresh = cv2.threshold(gray_image, 20, 255, cv2.THRESH_BINARY)
    cnt, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    hull = []
    hull.append(cv2.convexHull(cnt[0]))
    epsilon = 0.05*cv2.arcLength(hull[0], True)
    approx = cv2.approxPolyDP(hull[0], epsilon, True)
    pts1 = np.float32(approx)
    pts2 = np.ones(np.shape(pts1), dtype=np.float32)
    i, fin, min_dis = 0, 0, h+w
    for pt in pts1:
        if pt[0][0]+pt[0][1] < min_dis:
            fin = i
            min_dis = pt[0][0] + pt[0][1]
        i += 1
    i = 0
    for j in range(fin, np.shape(pts1)[0]) :
        pts2[i] = pts1[j]
        i += 1
    for j in range(0, fin):
        pts2[i] = pts1[j]
        i += 1
    pts1 = pts2
    pts2 = np.float32([[[0, 0]], [[h-1, 0]], [[h-1, w-1]], [[0, w-1]]])
    M = cv2.getPerspectiveTransform(pts1, pts2)
    warped = cv2.warpPerspective(image, M, (h, w))



    # debugging
    # hull_points = np.zeros(np.shape(image))
    # hull_shape = np.zeros(np.shape(image))
    # approx_poly = np.zeros(np.shape(image))
    # cv2.drawContours(hull_shape, cnt, 0, (0, 0, 255), 1)
    # for point in hull[0]:
    #     new_image = cv2.circle(hull_points, point[0], 2, (0,0,255), 2)
    # cv2.drawContours(approx_poly, [approx], 0, (0, 0, 255), 2)
    cv2.imshow("orginal image", image)
    # cv2.imshow("grayscale image", gray_image)
    # cv2.imshow("edges", edges)
    # cv2.imshow("segmented image", thresh)
    # cv2.imshow("hull points", hull_points)
    # cv2.imshow("hull shape", hull_shape)
    # cv2.imshow("approx poly", approx_poly)
    # cv2.imshow("final translation", warped)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



    ######################################################################

    warped = sol(warped)
    return warped

path = "./test/3.png"
solution(path)



