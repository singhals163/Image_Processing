import librosa
import librosa.display
import numpy as np
import cv2

def process_plot(file):
    audio_file = file
    y, sr = librosa.load(audio_file)
    # waveforms(y , sr)
    # spectrogram(y, sr)
    # spectrum(y, sr)
    mel_spec(y,sr)

def mel_spec(y, sr):
    mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr)

# Convert the power spectrogram to dB scale (decibels)
    mel_spectrogram_db = librosa.power_to_db(mel_spectrogram, ref=np.max)
    print(np.shape(mel_spectrogram_db))

    mel_spectrogram_normalized = np.uint8(((mel_spectrogram_db+80.0)*255.0)/80.0)
    print(mel_spectrogram_normalized[0])
    ref = np.zeros(np.shape(mel_spectrogram_normalized))
    # print(np.shape(ref))
    # (h, w) = np.shape(mel_spectrogram_normalized)
    # output_image = np.zeros((h, w, 3))
    # for i in range(h):
    #     for j in range(w):
    #         output_image[i][j][1] = mel_spectrogram_normalized[i][j]
    # mel_spectrogram_normalized = cv2.merge((ref, mel_spectrogram_normalized, ref))
    # print(output_image[64][10])
    # print(mel_spectrogram_normalized[64][10])
    cv2.imwrite("metal11.png", mel_spectrogram_normalized)
    cv2.imshow("output", mel_spectrogram_normalized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
process_plot("./test/metal_banging11.mp3")