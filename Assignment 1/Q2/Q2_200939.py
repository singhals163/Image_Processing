import cv2
import numpy as np
import librosa

def get_audio(file):
    audio_file = file
    y, sr = librosa.load(audio_file)
    return y, sr

############# using image analysis ##############
def mel_spec(y, sr):
    mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr)

    # Convert the power spectrogram to dB scale (decibels)
    mel_spectrogram_db = librosa.power_to_db(mel_spectrogram, ref=np.max)

    max_intensity = np.amax(mel_spectrogram_db)
    min_intensity = np.amin(mel_spectrogram_db)

    mel_spectrogram_normalized = np.uint8(((mel_spectrogram_db-min_intensity)*255.0)/(max_intensity - min_intensity))
    return mel_spectrogram_normalized

def process_image(image):
    # Define the contrast and brightness adjustments
    contrast_factor = 1.2
    brightness_factor = 0

    # Apply the contrast and brightness adjustments
    adjusted_image = cv2.convertScaleAbs(image, alpha=contrast_factor, beta=brightness_factor)
    gray = cv2.GaussianBlur(adjusted_image, (5,5), 1.0, sigmaY=1.0)

    canny = cv2.Canny(gray, 150, 180)
    mask = np.zeros(np.shape(canny))
    (h, w) = np.shape(mask)
    mask[3*h//4 : 7*h//8] = 1
    output = np.multiply(canny, mask)
    output = np.array(output, np.uint8)

    lines = cv2.HoughLines(output, rho=7, theta=np.pi/2, threshold=120)
    result = np.zeros(np.shape  (gray))
    count = 0
    # Draw the detected lines on the original image
    if lines is not None:
        for rho, theta in lines[:, 0]:
            if np.abs(theta - np.pi/2) < 1e-5:
                count += 1
            a, b = np.cos(theta), np.sin(theta)
            x0, y0 = a * rho, b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            cv2.line(result, (x1, y1), (x2, y2), 255, 2)
    # debugging
    # print(count)
    # cv2.imshow('Original Image', image)
    # cv2.imshow("contrast image", adjusted_image)
    # cv2.imshow("gauss", gray)
    # cv2.imshow("edges", canny)
    # cv2.imshow("lower edges", output)
    # cv2.imshow('Image with Lines', result)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    if count == 0:
        return "cardboard"
    return "metal"

def using_image(y, sr):
    mel_spec_image = mel_spec(y, sr)
    return process_image(mel_spec_image)

############# Using audio analysis ##############
def spectrum(y, sr):
    window_length = 5
    box_filter = np.ones(window_length) / (window_length)
    y = np.convolve(y, box_filter, mode='same')
    fft = np.fft.fft(y)
    magnitude = np.abs(fft)
    frequency = np.fft.fftfreq(len(magnitude), 1/sr)
    return np.abs(frequency[np.abs(np.argmax(magnitude))])

def using_audio(y, sr):
    spec = spectrum(y, sr)
    if spec < 400:
        return "cardboard"
    return "metal"

def solution(audio_path):
    ############################
    ############################

    ############################
    ############################
    ## comment the line below before submitting else your code wont be executed##
    # pass

    y, sr = get_audio(audio_path)

    class_name_image = using_image(y, sr)
    # print(audio_path, class_name_image)
    class_name_audio = using_audio(y, sr)
    if class_name_audio != class_name_image:
        return class_name_audio
    return class_name_audio