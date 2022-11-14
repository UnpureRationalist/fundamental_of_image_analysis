import cv2
import numpy as np


from PIL import Image
import matplotlib.pyplot as plt

# 仿真运动模糊
def motion_process(len, size):
    sx, sy = size
    PSF = np.zeros((sy, sx))
    PSF[int(sy / 2):int(sy / 2 + 1), int(sx / 2 - len / 2)
            :int(sx / 2 + len / 2)] = 1
    return PSF / PSF.sum()  # 归一化亮度


def make_blurred(input, PSF, eps):
    input_fft = np.fft.fft2(input)
    PSF_fft = np.fft.fft2(PSF) + eps
    blurred = np.fft.ifft2(input_fft * PSF_fft)
    blurred = np.abs(np.fft.fftshift(blurred))
    return blurred


def wiener(input, PSF, eps):
    input_fft = np.fft.fft2(input)
    PSF_fft = np.fft.fft2(PSF) + eps  # 噪声功率，这是已知的，考虑epsilon
    result = np.fft.ifft2(input_fft / PSF_fft)  # 计算F(u,v)的傅里叶反变换
    result = np.abs(np.fft.fftshift(result))
    return result


image = Image.open('imgs/Lenna.jpg').convert('L')
plt.figure(1)
plt.xlabel("Original Image")
plt.gray()
plt.imshow(image)

plt.figure(2)
plt.gray()
data = np.asarray(image.getdata()).reshape(image.size)
PSF = motion_process(30, data.shape)
blurred = np.abs(make_blurred(data, PSF, 1e-3))

plt.subplot(221)
plt.xlabel("Motion blurred")
plt.imshow(blurred)

result = wiener(blurred, PSF, 1e-3)
plt.subplot(222)
plt.xlabel("wiener deblurred")
plt.imshow(result)

blurred += 0.04 * blurred.std() * np.random.standard_normal(blurred.shape)

plt.subplot(223)
plt.xlabel("motion & noisy blurred")
plt.imshow(blurred)

result = wiener(blurred, PSF, 0.1 + 1e-3)
plt.subplot(224)
plt.xlabel("wiener deblurred")
plt.imshow(result)

plt.show()
