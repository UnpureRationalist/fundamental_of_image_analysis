import sys

import cv2
from albumentations import HorizontalFlip, VerticalFlip, Rotate, ShiftScaleRotate


# 平移
def shift(img):
    transform = ShiftScaleRotate(shift_limit=0.5, 
                                scale_limit=0, 
                                rotate_limit=0, 
                                interpolation=cv2.INTER_CUBIC,
                                p=1.0)
    return transform(image=img)['image']


# 水平镜像
def horizonal(img):
    transform = HorizontalFlip(p=1.0)
    return transform(image=img)['image']


# 竖直镜像
def vertical(img):
    transform = VerticalFlip(p=1.0)
    return transform(image=img)['image']

# 旋转
def rotate(img):
    transform = Rotate(interpolation=cv2.INTER_CUBIC, p=1.0)
    return transform(image=img)['image']


mp = {
    'shift': shift,
    'horizonal': horizonal,
    'vertical': vertical,
    'rotate': rotate
}


def geometric_operation(oper_name, img):
    return mp[oper_name](img)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python geometric_operation.py image_path geometric_operation1 [geometric_operation2 ...]')
        exit(-1)
    
    file_name = sys.argv[1]
    img = cv2.imread(file_name)

    operations = []
    for i in range(2, len(sys.argv)):
        operations.append(sys.argv[i])
    
    for operation in operations:
        if operation not in mp.keys():
            print('Not support geometric operation type:', operation)
            print('Support geometric operation includes:')
            print('- shift')
            print('- horizonal')
            print('- vertical')
            print('- rotate')
            exit(-1)
    for operation in operations:
        img = geometric_operation(operation, img)


    cv2.namedWindow('handled image')
    cv2.imshow('handled image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
