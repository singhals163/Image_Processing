import cv2
import numpy as np



def spatial_kernel_function(x, y, sigma_spatial, spatial_kernel_size):
    return np.exp(-((x - (spatial_kernel_size-1)/2)**2 + (y - (spatial_kernel_size-1)/2)**2) / (2 * sigma_spatial**2))

def joint_bilateral_filter_rgb(target_image, guidance_image, sigma_spatial=1, sigma_range=1):

    # spatial_kernel_size = 15
    # spatial_kernel = np.fromfunction(
    #     lambda x, y: np.exp(-((x - (spatial_kernel_size-1)/2)**2 + (y - (spatial_kernel_size-1)/2)**2) / (2*sigma_spatial**2)),
    #     (spatial_kernel_size, spatial_kernel_size)
    # )
    # spatial_kernel = spatial_kernel / np.sum(spatial_kernel)
    spatial_kernel_size = 15
    spatial_kernel = np.fromfunction(np.vectorize(spatial_kernel_function), (spatial_kernel_size, spatial_kernel_size), sigma_spatial=sigma_spatial,spatial_kernel_size = spatial_kernel_size)
    spatial_kernel = np.stack((spatial_kernel, spatial_kernel, spatial_kernel), axis=2)
    # spatial_kernel = spatial_kernel / np.sum(spatial_kernel)
    height, width, channel = target_image.shape
    filtered_image = np.zeros_like(target_image[:,:,0], dtype=np.float64)

    target_image = np.float64(target_image)
    guidance_image = np.float64(guidance_image)

    rgb_final = np.zeros_like(target_image, dtype=np.float64)
    # for c in range(channel):
    for i in range(height):
        for j in range(width):
            i_min = max(0, i - spatial_kernel_size // 2)
            i_max = min(height, i + spatial_kernel_size // 2 + 1)
            j_min = max(0, j - spatial_kernel_size // 2)
            j_max = min(width, j + spatial_kernel_size // 2 + 1)
            target_patch = target_image[i_min:i_max, j_min:j_max, :]
            
            guidance_patch = guidance_image[i_min:i_max, j_min:j_max, :]
            range_kernel = np.exp(-(target_patch - target_image[i, j, :])**2 / (2*sigma_range**2))

            # print(spatial_kernel[:i_max-i_min, :j_max-j_min].shape, range_kernel.shape)
            filter_response = spatial_kernel[:i_max-i_min, :j_max-j_min, :] * range_kernel
            val = filter_response * guidance_patch
            for c in range(3):
                rgb_final[i,j,c] = np.sum(val[:,:,c])/np.sum(filter_response[:,:,c])
            # filter_response = filter_response / np.sum(filter_response)
            # filtered_image[i, j] = np.sum(filter_response * guidance_patch)


    return rgb_final.astype(np.uint8)

def solution(image_path_a, image_path_b):
    ############################
    ############################
    ## image_path_a is path to the non-flash high ISO image
    ## image_path_b is path to the flash low ISO image
    ############################
    ############################
    target_image = cv2.imread(image_path_b)
    guidance_image = cv2.imread(image_path_a)
    filtered_image_rgb = joint_bilateral_filter_rgb(target_image, guidance_image, sigma_spatial=15, sigma_range=1)
    return filtered_image_rgb

# img = solution("./ultimate_test/2_a.jpg", "./ultimate_test/2_b.jpg")
# cv2.imshow("HERE", img)
# cv2.waitKey()
# cv2.destroyAllWindows()