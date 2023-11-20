## Assignment 2
This folder contains the solution of Assignment 2 problems. The idea of the implementation were as follows:

### Q1
The initial analysis of the problem suggested to the thresholding of the lava images in the HSV color space. This is because in the image containing the lava, the scenes except lava are that of rocks which are black and thus thresholding was the obvious choice. The original image was converted into HSV space and thresholds were applied to each channels separately and later the and of these channels was taken in order to create the mask of the lava in the image.

### Q2
This was a comparatively simpler question in which we had to implement the cross-bilateral filter. The major challenge was to decrease the time taken by the bilateral filter to work on an image, and although the ideal technique would be to implement a parallel program for the algorithm, the time was reduced by using highly optimised vector arithmatic implemented in numpy library which led to computing output for the correct image in almost 40s on a Mac M2.

### Q3
After trying segmentation and using haar-cascade feature matching of Ravana's face, and failing at multiple levels, the only way left was to store the image in the code and compare the given input image to the saved image to check if the ravana matched any of the given real ravana templates.

:)