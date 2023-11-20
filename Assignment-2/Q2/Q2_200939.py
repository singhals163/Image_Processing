import cv2
import numpy as np

def gauss_kernel(k, sig):
    x = np.linspace(-(k//2), (k//2), k)
    gx, gy = np.meshgrid(x, x)
    kernel = np.exp(-1*(gx**2 + gy**2)/(2*(sig**2)))
    return kernel

def cross_bilateral_filter_colored(input_image, guide_image, sigma_spatial, sigma_range, window_size):
    input_image = np.float64(input_image)
    guide_image = np.float64(guide_image)
    half_window = window_size // 2
    spacial_filter = gauss_kernel(window_size, sigma_spatial)
    spacial_filter = np.stack((spacial_filter, spacial_filter, spacial_filter), axis=2)

    padded_input = np.pad(input_image, ((half_window, half_window), (half_window, half_window), (0, 0)), mode='reflect')

    padded_guidance = np.pad(guide_image, ((half_window, half_window), (half_window, half_window), (0, 0)), mode='reflect')
    # print(padded_guidance.dtype)  

    output_image = np.zeros_like(input_image, dtype=np.float64)
    for y in range(input_image.shape[0]):
        for x in range(input_image.shape[1]):
            I_p = guide_image[y][x]
            y_min = y
            y_max = y + window_size
            x_min = x
            x_max = x + window_size
                        
            range_filter = padded_guidance[y_min:y_max, x_min:x_max, :]
            range_filter = (range_filter) - (I_p)
            range_filter = np.exp(-0.5 * ((range_filter) ** 2) / (sigma_range ** 2))

            bilateral_mask = range_filter * spacial_filter
            image_window = padded_input[y_min:y_max, x_min:x_max, :]
            value = image_window * bilateral_mask

            for c in range(3):
                # v = np.sum(value[:, :, c])
                # normality = np.sum(bilateral_mask[:, :, c])
                # output_image[y, x, c] = v / normality
                output_image[y, x, c] = np.sum(value[:, :, c]) / np.sum(bilateral_mask[:, :, c])
    return output_image.astype(np.uint8)



def solution(image_path_a, image_path_b):
    ############################
    ############################
    ## image_path_a is path to the non-flash high ISO image
    ## image_path_b is path to the flash low ISO image
    ############################
    ############################
    ## comment the line below before submitting else your code wont be executed##
    # pass
    no_flash = cv2.imread(image_path_a)
    flash = cv2.imread(image_path_b)
    return cross_bilateral_filter_colored(no_flash, flash, 15, 0.5, 15)