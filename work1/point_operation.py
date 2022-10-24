import os
import sys
import cv2
import numpy as np


# 线性点运算(增大对比度)
def linear_point_operation(num):
    num = 1.5 * num
    if num >= 255:
        num = 255
    return int(num)


# 分段线性点运算
def segment_point_operation(num, a=80, k1=0.5):
    assert 0 <= a <= 120
    b = 255 - a
    k2 = (255 - 2 * k1 * a) / (b - a)
    b2 = a * (k1 - k2)
    res = 0
    if num <= a:
        res = k1 * num
    elif num <= b:
        res = k2 * num + b2
    else:
        res = 255 - k1 * (255 - num)
    res = int(res)
    return res


# 非线性点运算
def non_linear_point_operation(num):
    res = num ** 2.5 / 4072
    # res = 32 * np.log2(1 + num)
    if res >= 255:
        res = 255
    res = int(res)
    return res


def point_operation(img, transform):
    trans_img = np.zeros_like(img, dtype=np.uint8)
    assert len(img.shape) == 2
    for i in range(len(img)):
        for j in range(len(img[i])):
            trans_img[i][j] = transform(img[i][j])
    return trans_img



if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python point_operation.py image_path operation_type')
        exit(-1)
    file_name = sys.argv[1]
    img = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE)
    oper_type = sys.argv[2]
    po_fun = None
    if oper_type == 'linear':
        po_fun = linear_point_operation
    elif oper_type == 'segment':
        po_fun = segment_point_operation
    elif oper_type == 'non_linear':
        po_fun = non_linear_point_operation
    else:
        print('Not support point operation type:', oper_type, ', support operation includes:')
        print('- linear')
        print('- segment')
        print('- non_linear')
        exit(-1)
    trans_img = point_operation(img, po_fun)
    base_name = os.path.basename(file_name)
    root = os.path.dirname(file_name)
    write_path = os.path.join(root, oper_type + '_' + base_name)
    cv2.imwrite(write_path, trans_img)

    print('Handled image saved in:', write_path)
