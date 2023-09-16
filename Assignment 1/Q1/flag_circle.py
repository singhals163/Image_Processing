import cv2
import numpy as np

image = cv2.imread("./ground truth/1.png")
new_image = image[199:400][:][:]
new_image = new_image[:, 199:400, :]
(H, W, _) = np.shape(new_image)
for i in range(H):
    print("[", end=" ")
    for j in range(W):
        print("[", end = "")
        for k in range(2):
            print(new_image[i][j][k], end=", ")
        if j < W-1:
            print(new_image[i][j][2], end="], ")
        else:
            print(new_image[i][j][2], end="] ")
    print("],")


# print(new_image)
cv2.imshow("curr image", new_image)
cv2.waitKey(0)
cv2.destroyAllWindows()