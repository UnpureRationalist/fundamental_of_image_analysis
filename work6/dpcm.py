import sys

import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import peak_signal_noise_ratio as psnr


def quant(bit, error):
    return (error + 255) / (2 ** (9 - bit))


def rev_quant(bit, pred):
    return pred * (2 ** (9 - bit)) - 255


def DPCM(img, bit):
    cons_img = np.zeros_like(img)
    diff_img = np.zeros_like(img)

    width, height = img.shape
    for j in range(height):
        for i in range(width):
            if j == 0:
                error = img[i][j] - 128
                diff_img[i][j] = quant(bit, error)
                cons_img[i][j] = rev_quant(bit, diff_img[i][j]) + 128
            else:
                error = int(img[i][j]) - int(cons_img[i][j - 1])
                diff_img[i][j] = quant(bit, error)
                cons_img[i][j] = rev_quant(bit, diff_img[i][j]) + cons_img[i][j - 1]

    return cons_img, diff_img


def error():
    print('Usage:')
    print('python .\dpcm.py image_path bit')
    exit(-1)


if __name__ == '__main__':
    image_path = None
    bit = None
    if len(sys.argv) != 3:
        error()
    try:
        image_path = sys.argv[1]
        bit = int(sys.argv[2])
    except:
        error()

    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    cons_img, diff_img = DPCM(img, bit)

    psnr_val = psnr(img, cons_img)
    ssim_val = ssim(img, cons_img)
    print('PSNR =', psnr_val, ' SSIM =', ssim_val)

    cv2.imshow('original', img)
    cv2.imshow(f'construct_{bit}_bit', cons_img)
    cv2.imshow(f'differ_{bit}_bit', diff_img)
    cv2.waitKey()
