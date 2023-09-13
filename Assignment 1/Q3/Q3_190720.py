import cv2
import numpy as np
import math

def solution(image_path):
    ############################
    ############################

    ############################
    ############################
    ## comment the line below before submitting else your code wont be executed##
    # pass
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7,7), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    thresh = cv2.dilate(thresh, kernel, iterations=2)

    # Find contours and sort for largest contour
    cnts, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    c = max(cnts, key=cv2.contourArea)
    # cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    # cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    # displayCnt = None

    # for c in cnts:
    #     # Perform contour approximation
    #     peri = cv2.arcLength(c, True)
    #     approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    #     if len(approx) == 4:
    #         displayCnt = approx
    #         break
    M = cv2.moments(c)
    if M['m00'] != 0:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
    rows,cols = gray.shape[:2]
    [vx,vy,x,y] = cv2.fitLine(c, cv2.DIST_L2,0,0.01,0.01)
    lefty = int((-x*vy/vx) + y)
    righty = int(((cols-x)*vy/vx)+y)
    thresh = cv2.line(thresh,(cols-1,righty),(0,lefty),(0,255,0),2)
    print(math.degrees(math.atan(-vy/vx)))
    translated_image = np.uint8(np.ones(np.shape(image)) * 255)
    print(rows, cols, cx, cy)
    x_trans = cols//2 - cx
    y_trans = rows//2 - cy
    print(x_trans, y_trans)
    for i in range(max(0, -x_trans), min(cols-1, cols - x_trans)):
        for j in range(max(0, -y_trans), min(rows-1, rows - y_trans)):
            if j + y_trans >= rows-1 or i + x_trans >= cols-1:
                continue
            translated_image[j + y_trans][i + x_trans] = image[j][i]
    angle = math.degrees(math.atan(vy/vx))
    if abs(angle) < 4:
        angle = 0
    rotation_matrix = cv2.getRotationMatrix2D((cols//2-10, rows//2-15), angle, scale=1.0)
    rotated = cv2.warpAffine(image, rotation_matrix, (cols, rows), borderValue=(255, 255, 255))
    # rect = cv2.minAreaRect(c)
    # box = cv2.boxPoints(rect)
    # box = np.int0(box)
    # print(box)
    # thresh = cv2.drawContours(thresh,[box],0,(0,0,255),2)

    # Obtain birds' eye view of image
    # warped = cv2.four_point_transform(image, displayCnt.reshape(4, 2))

    # cv2.imshow("warped", warped)
    # # debugging
    # hull_points = np.zeros(np.shape(image))
    hull_shape = np.zeros(np.shape(image))
    cv2.drawContours(hull_shape, [c], 0, (0, 0, 255), 1)
    # # approx_poly = np.zeros(np.shape(image))
    # for point in hull[0]:
    #     new_image = cv2.circle(hull_points, point[0], 2, (0,0,255), 2)
    # # cv2.drawContours(approx_poly, [approx], 0, (0, 0, 255), 2)
    cv2.imshow("orginal image", image)
    cv2.imshow("hull shape", hull_shape)
    cv2.imshow("thresh", thresh)
    cv2.imshow("translated", translated_image)
    cv2.imshow("rotated", rotated)
    # cv2.imshow("grayscale image", image_gray)
    # cv2.imshow("edges", edges)
    # cv2.imshow("segmented image", thresh)
    # cv2.imshow("hull points", hull_points)
    # # cv2.imshow("approx poly", approx_poly)
    # # cv2.imshow("final translation", warped)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # return image

image_path = "./test/3_a.png"
solution(image_path)