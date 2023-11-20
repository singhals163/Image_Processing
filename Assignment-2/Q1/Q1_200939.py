import cv2
import numpy as np


def separate_hsv(image) :
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    h, s, v = cv2.split(hsv_image)
    h = np.clip(h, 0, 255)
    _, thresh_H = cv2.threshold(h, 35, 255, cv2.THRESH_BINARY_INV)
    _, thresh_S = cv2.threshold(s, 128, 255, cv2.THRESH_BINARY)
    _, thresh_V = cv2.threshold(v, 128, 255, cv2.THRESH_BINARY)
    mask = thresh_H & thresh_S & thresh_V

    kernel_size = 3  
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    # closed_image = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
    # closed_image = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=5)
    # closed_image = cv2.morphologyEx(closed_image, cv2.MORPH_OPEN, kernel, iterations=1)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
    # largest_5_contours = sorted_contours[:3]
    contour_image = np.zeros_like(image)
    cv2.drawContours(contour_image, contours, -1, (255, 255, 255), cv2.FILLED)
    return contour_image

# Usage
def solution(image_path):
    ######################################################################
    ######################################################################
    '''
    The pixel values of output should be 0 and 255 and not 0 and 1
    '''
    #####  WRITE YOUR CODE BELOW THIS LINE ###############################
    image = cv2.imread(image_path)
    image = separate_hsv(image)
    ######################################################################  
    return image