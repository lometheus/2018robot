#-*-coding=utf-8-*-
from collections import  deque
import numpy as np
import cv2
import time
import qrcode
import os
from PIL import Image
import zxing
import random
import logging
import math
strand_dis=20
strand_ran=160

logger=logging.getLogger(__name__)
if not logger.handlers :logging.basicConfig(level=logging.INFO)
DEBUG= (logging.getLevelName(logger.getEffectiveLevel())=='DEBUG')

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # L、M、H、Q几个级别
    box_size=10,
    border=4, )
def dis(a,b):
    return math.sqrt(math.pow((a[0] - b[0]), 2) + math.pow((a[1] - b[1]), 2))

def calculate(point):

    len=dis(point[0],point[1])
    len2 = dis(point[2], point[3])
    distant=strand_ran*strand_dis/len+strand_ran*strand_dis/len2#计算左右两个高，根据比例算出直线距离
    print ( distant/2)
    len3 = dis(point[0], point[3])
    len4 = dis(point[2], point[1])
    if len>len2:
        print("left")
    elif len2>len:
        print("right")
    else:
        print("center")
    len3=(len3 + len4) / 2
    len=(len2+len)/2
    if len3<len:
        print(math.acos(len3/len))#以弧度方式输出角度





def ocr_qrcode_zxing(filename):

    img = Image.open(filename)
    ran = int(random.random() * 100000)
    img.save('%s%s.jpg' % (os.path.basename(filename).split('.')[0], ran))
    zx = zxing.BarCodeReader()
    data = ''
    zxdata = zx.decode('%s%s.jpg' % (os.path.basename(filename).split('.')[0], ran))
    # 删除临时文件
    os.remove('%s%s.jpg' % (os.path.basename(filename).split('.')[0], ran))
    if zxdata:
        #logger.debug(u'zxing识别二维码:%s,内容: %s' %(filename ,zxdata.data))
        print(zxdata.points)
        if(len(zxdata.points)):
            calculate(zxdata.points)
        '''class BarCode:
	  format = ""
	  四个角位置points = [leftdown,lefton,righton,rightdown]
	  data = ""
	  读取的内容raw = ""'''
        #data = zxdata.data
    else:
        logger.error(u'识别zxing二维码出错:%s' %(filename))
        img.save('%s-zxing.jpg' %filename)
    return data


if __name__ == '__main__':
    cap= cv2.VideoCapture(0)
    #filename =r'xinxingzhao.png'
    while True:
        ret, frame = cap.read()
        cv2.imwrite("temp.jpg", frame)
        ltext = ocr_qrcode_zxing('temp.jpg')


    #生成二维码
    '''qr.add_data('robo')
    qr.make(fit=True)
    img = qr.make_image()
    img.save('robo.png')
'''
