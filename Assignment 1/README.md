## Assignment 1
This folder contains the solution for Assignment 1. Brief explanation of my implementations for all three questions:

### Q1
In Q1, the task was to find the orientation of Indian national flag, and fit it to the image size and return a $600\times 600$ image containing the final flag. This was done using two techniques:
- Using perspective transform
  1. Find the corner points of the flag using the convex hull and approximate the hull to get only 4 points
  2. Apply perspective transform on these four points by calculating their rotational matrix and thus transform the image to a full sized window containg only the flag 
  3. Further find what all colors are present on the corners and return the flag appropriately
- Using center of mass of all the points belonging to diffent colours
  1. Find the centroid of green and saffron colors
  2. Figure out the orientation of the flag using the diffence between the centroids of the two colors
  3. Return the flag appropriately
#### Comparison of the two approaches
However both the approaches gave correct results on the test cases provided, the second one seems to be more robust for this problem, this is because the first approach may not yield 4 points after approximating the hull sometimes, which will lead to erroneous results

### Q2
The task was to figure out which sound belonged to the cardboard and which one to the metal. Two methods were explored for the same. One of the crucial thing to notice was that there was a high frequency harmonic present in the case of metal banging which wasn't there for the carboard sound.
- Using Image processing
  1. The idea was to somehow find that horizontal line in the mel spectrogram which was there in the lower half(corresponding to higher frequency)
  2. For this the image was smoothened and the contrast was enhanced and later, canny edge detector was applied to find the edges in the image consisting of pixel values as the power corresponding to various frequencies present in the mel spectrogram of the sound
  3. A mask was applied in the lower half of the image
  4. Using Hough transform horizontal lines were extracted in the desired region
  5. if such a line was present, the answer was reported as yes else no
- Using signal processing
  1. The signal was smoothened to remove noice
  2. The fundamental frequency was calculated for all the sounds using only the spectrum of the whole sound
  3. The fundamental frequency was higher for metal banging as compared to cardboard
        - metal - $517\ Hz$
        - carboard $\approx 100-200\ Hz$
  4. Appropriate threshold was applied to find this fundamental frequency and the answer was reported accordingly

#### Comparison of the two approaches
The second approach was more robust as the higher frequency which was used to classify the sound was sometimes not so evident in the mel spectrogram and thus may lead to wrong answers in some cases. Even smoothening the audio signal before taking the mel spectrogram of the audio would only decrease its power and thus the line would become even hard to detect. Apart from that Hough transform in the required region would sometimes produce a horizontal line in the case of a cardboard as well based on the threshold set for the number of lines that should belong to make a line strong.

The second approach however was more robust and thus was used to report the answer

### Q3
The task was to detect the orientation of a Sanskrit Shloka and rotate it to orient it in the direction of normal reading. The method used was as follows:
1. Increase the size of the image by adding white border so that the text would always fit in the image after rotating it
1. Dilate the image using morphological operations to increase the area of text and make it continuous
2. Find the contour of the image
3. Find the center of the contour and translate the image to match the center of the contour with that of the image
5. Find the best fit line of this contour and rotate the image to make the slope of this line 0
6. Apply Radon transform to make sure that the image is completely horizontal. This would make the image horizontal if the tilt of the shloka after rotating in the previous step belonged to $(-10\degree, 10\degree)$
7. Find continously occuring 25 pixels horizontally and call it a line that is present over the text in Devnagiri script. Find the number of white pixels in a $10$ pixel high box above and below this line.
8. If the number of white pixels above are more, return the image from step $6^{th}$ step else rotate the by $180\degree$ and then return the image

:)