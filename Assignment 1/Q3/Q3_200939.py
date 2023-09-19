import cv2
import numpy as np
from skimage.transform import radon
import math

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)
    return thresh

def translate_image(image, cx, cy):
    translated_image = np.uint8(np.ones(np.shape(image)) * 255)
    (rows, cols, _) = np.shape(image)
    # print(rows, cols, cx, cy)
    x_trans = cols//2 - cx
    y_trans = rows//2 - cy
    # print(x_trans, y_trans)
    for i in range(max(0, -x_trans), min(cols-1, cols - x_trans)):
        for j in range(max(0, -y_trans), min(rows-1, rows - y_trans)):
            if j + y_trans >= rows-1 or i + x_trans >= cols-1:
                continue
            translated_image[j + y_trans][i + x_trans] = image[j][i]
    return translated_image

def rotate_image(image):

    thresh = preprocess_image(image)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    thresh = cv2.dilate(thresh, kernel, iterations=2)

    # Find contours and sort for largest contour
    cnts, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    c = max(cnts, key=cv2.contourArea)
    M = cv2.moments(c)
    if M['m00'] != 0:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
    translated_image = translate_image(image, cx, cy)

    (rows,cols) = np.shape(thresh)

    [vx,vy,x,y] = cv2.fitLine(c, cv2.DIST_L2,0,0.01,0.01)
    lefty = int((-x*vy/vx) + y)
    righty = int(((cols-x)*vy/vx)+y)
    thresh = cv2.line(thresh,(cols-1,righty),(0,lefty),(0,255,0),2)
    # print(math.degrees(math.atan(-vy/vx)))

    angle = math.degrees(math.atan(vy/vx))
    if np.abs(angle) < 4:
        angle = 0
    rotation_matrix = cv2.getRotationMatrix2D((cols//2, rows//2), angle, scale=1.0)
    rotated = cv2.warpAffine(image, rotation_matrix, (cols, rows), borderValue=(255, 255, 255))
    hull_shape = np.zeros(np.shape(image))
    cv2.drawContours(hull_shape, [c], 0, (0, 0, 255), 1)

    return rotated

def deskew_image(image):
    temp_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (H, W) = np.shape(temp_image)
    normalized_image = temp_image - np.mean(temp_image)
    sinogram = radon(normalized_image)
    projection_profile = np.array([np.sqrt(np.mean(np.abs(line) ** 2)) for line in sinogram.transpose()])
    rotation_angle = np.argmax(projection_profile)

    # Calculate the rotation matrix
    center = (W // 2, H // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, 90 - rotation_angle, 1)
    rotated_image = cv2.warpAffine(image, rotation_matrix, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))
    
    return rotated_image


def add_borders(image):
    (H, W, _) = np.shape(image)
    increase_size = H//4
    new_image = np.uint8(np.ones((H + increase_size, W + increase_size, 3))*255)
    for i in range(increase_size//2, H + increase_size//2):
        new_image[i][increase_size//2:W+increase_size//2][:] = image[i-increase_size//2][:][:]
    return new_image

def check_up(image, row, H, W):
    window = 10
    count_up = 0
    # print(row)
    for i in range(max(0, row - window),row):
        for j in range(W):
            if image[i][j] == 0:
                count_up += 1
    count_down = 0
    for i in range(row+1, min(H, row+window+1)):
        for j in range(W):
            if image[i][j] == 0:
                count_down += 1
    return count_up - count_down

def check_inverted(image):
    temp = preprocess_image(image)
    (H, W) = np.shape(temp)
    count = 0
    flag = 0
    for i in range(10, H-10):
        for j in range(W):
            if temp[i][j] == 255:
                count += 1
            else:
                count = 0
            if count == 25:
                flag += check_up(temp, i, H, W)
                break
    if flag > 0:
        return image
    return cv2.rotate(image, cv2.ROTATE_180)


def correct_alignment(image_path):
    image = cv2.imread(image_path)
    image = add_borders(image)
    image = rotate_image(image)
    image = rotate_image(image)
    image = deskew_image(image)
    image = check_inverted(image)
    # cv2.imshow("image", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return image

def solution(image_path):
    ############################
    ############################

    ############################
    ############################
    ## comment the line below before submitting else your code wont be executed##
    # pass
    return correct_alignment(image_path)