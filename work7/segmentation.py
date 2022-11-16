import os
import sys
import time

import cv2
import numpy as np


L = 256

def get_img_info(img):
    pixel_counts = np.zeros(L, dtype=np.int32)
    for i in range(len(img)):
        for j in range(len(img[i])):
            pixel_counts[img[i][j]] += 1
    total_pixels = img.shape[0] * img.shape[1]
    probs = pixel_counts / total_pixels
    indices = np.arange(L)
    avg = np.sum(probs * indices)   # 平均灰度级
    return avg, probs


def cal_class_norm(k, probs, u, w0, w1):
    indices = np.arange(L)
    u0 = np.sum(indices[:k] * probs[:k]) / w0
    u1 = np.sum(indices[k:] * probs[k:]) / w1
    return w0 * (u - u0)**2 + w1 * (u - u1)**2


def cal_class_mean(k, probs, w0, w1):
    indices = np.arange(L)
    u0 = np.sum(indices[:k] * probs[:k]) / w0
    u1 = np.sum(indices[k:] * probs[k:]) / w1
    return u0, u1


def ostf_seg(img):
    avg, probs = get_img_info(img)
    max_score = -1
    sel_k = -1
    for k in range(L):
        w0 = np.sum(probs[:k])
        w1 = 1 - w0
        if w0 == 0 or w1 == 0:
            continue
        score = cal_class_norm(k, probs, avg, w0, w1)
        if score > max_score:
            max_score = score
            sel_k = k
    seg_img = img > sel_k
    seg_img = seg_img.astype(np.uint8)
    seg_img[seg_img == 1] = L - 1
    return seg_img



def iter_seg(img, epsilon=1):
    avg, probs = get_img_info(img)
    pixel_set = []
    for i, prob in enumerate(probs):
        if prob != 0:
            pixel_set.append(i)
    begin = 0
    end = len(pixel_set) - 1
    mid = (begin + end) // 2
    k = pixel_set[mid]
    while begin < end:
        w0 = np.sum(probs[:k])
        w1 = 1 - w0
        if w0 == 0 or w1 == 0:
            continue
        u0, u1 = cal_class_mean(k, probs, w0, w1)
        next_k = int((u0 + u1) / 2)
        if abs(next_k - k) < epsilon:
            break
        else:
            k = next_k
    sel_k = k
    seg_img = img > sel_k
    seg_img = seg_img.astype(np.uint8)
    seg_img[seg_img == 1] = L - 1
    return seg_img


def error():
    print('Usage:')
    print('python .\segmentation.py image_path oper_type')
    exit(-1)


if __name__ == '__main__':
    image_path = None
    oper_type = None
    if len(sys.argv) != 3:
        error()
    try:
        image_path = sys.argv[1]
        oper_type = sys.argv[2]
    except:
        error()
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    seg_img = None
    if oper_type == 'ostf':
        seg_img = ostf_seg(img)
    elif oper_type == 'iter':
        seg_img = iter_seg(img)
    else:
        print(oper_type, 'is not supported segment algorithm!')
        print('ostf and iter are supported.')
        exit(-1)
    base_name = os.path.basename(image_path)
    root = os.path.dirname(image_path)
    write_name = os.path.join(root, oper_type + '_' + base_name)
    cv2.imwrite(write_name, seg_img)
