import os
import sys
import math

import cv2
import numpy as np


# 根据论文公式 5 获取暗通道
def get_dark_channel(img, size):
    blue, green, red = cv2.split(img)
    dark_channel = cv2.min(cv2.min(red, green), blue)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (size, size))
    dark = cv2.erode(dark_channel, kernel)
    return dark


# 估算全球大气光成分
def get_atmospheric_light(img, dark):
    [h, w] = img.shape[:2]
    img_size = h * w
    numpx = int(max(math.floor(img_size / 1000), 1))
    darkvec = dark.reshape(img_size)
    imvec = img.reshape(img_size, 3)

    indices = darkvec.argsort()
    indices = indices[img_size - numpx::]

    atmsum = np.zeros([1, 3])
    for ind in range(1, numpx):
       atmsum = atmsum + imvec[indices[ind]]

    A = atmsum / numpx
    return A


def estimate_transmission(img, A, size):
    omega = 0.95
    im3 = np.empty(img.shape, img.dtype)

    for ind in range(0, 3):
        im3[:, :, ind] = img[:, :, ind] / A[0, ind]

    transmission = 1 - omega * get_dark_channel(im3, size)
    return transmission


def guided_filter(img, p, r, eps):
    mean_I = cv2.boxFilter(img, cv2.CV_64F, (r, r))
    mean_p = cv2.boxFilter(p, cv2.CV_64F, (r, r))
    mean_Ip = cv2.boxFilter(img * p, cv2.CV_64F, (r, r))
    cov_Ip = mean_Ip - mean_I * mean_p

    mean_II = cv2.boxFilter(img * img, cv2.CV_64F, (r, r))
    var_I   = mean_II - mean_I * mean_I

    a = cov_Ip / (var_I + eps)
    b = mean_p - a * mean_I

    mean_a = cv2.boxFilter(a, cv2.CV_64F, (r, r))
    mean_b = cv2.boxFilter(b, cv2.CV_64F, (r, r))

    q = mean_a * img + mean_b
    return q


def refine_transmission(img, et):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = np.float64(gray) / 255
    r = 60
    eps = 0.0001
    t = guided_filter(gray, et, r, eps)

    return t


# 根据公式 1 复原图像
def recover(img, t, A, tx=0.1):
    res = np.empty(img.shape, img.dtype)
    t = cv2.max(t, tx)

    for ind in range(0, 3):
        res[:, :, ind] = (img[:, :, ind] - A[0, ind]) / t + A[0, ind]

    return res


def haze_removal(file_name):
    src = cv2.imread(file_name)
    
    I = src.astype('float64') / 255   # uint8 -> float64
    size = 15
    dark = get_dark_channel(I, size)
    A = get_atmospheric_light(I, dark)
    te = estimate_transmission(I, A, size)
    t = refine_transmission(src, te)
    J = recover(I, t, A, 0.1)

    # cv2.imshow("dark", dark)
    # cv2.imshow("t", t)
    cv2.imshow('original_image', src)
    cv2.imshow('recover_image', J)

    base_name = os.path.basename(file_name)
    write_name = file_name.replace(base_name, 'remove_' + base_name)

    cv2.imwrite(write_name, J * 255)
    cv2.waitKey()


if __name__ == '__main__':
    file_lst = []
    try:
        file_name = sys.argv[1]
        file_lst.append(file_name)
    except:
        root = './imgs/'
        file_lst = os.listdir(root)
        file_lst = [os.path.join(root, file) for file in file_lst if file[:6] != 'remove']

    for file_name in file_lst:
        haze_removal(file_name)
    