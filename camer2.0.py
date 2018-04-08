#coding:utf-8
from collections import  deque
import numpy as np
import cv2
import time

mode_y=60#已测量球和电脑的距离
sp_x=640
sp_x_1=70#该距离下球所占像素
#设定色阈值，HSV空间
bluLower = np.array([100, 100, 100])
bluUpper = np.array([125, 255, 255])
yelLower = np.array([26, 43, 46])
yelUpper = np.array([34, 255, 255])
#初始化追踪点的列表

def getcolor(Lower,Upper):
    (ret, frame) = camera.read()
    if not ret:
        print 'No Camera'
        return False

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, Lower, Upper)
    # 腐蚀操作
    mask = cv2.erode(mask, None, iterations=2)
    # 膨胀操作，其实先腐蚀再膨胀的效果是开运算，去除噪点
    mask = cv2.dilate(mask, None, iterations=2)
    # 轮廓检测
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    # 初始化瓶盖圆形轮廓质心
    # 如果存在轮廓
    if len(cnts) > 0:
        # 找到面积最大的轮廓
        c = max(cnts, key=cv2.contourArea)
        # 确定面积最大的轮廓的外接圆
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        if radius > 100:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.imshow('Frame', frame)
            return radius



'''小球的颜色，最好是蓝紫色或者红色，如果是均匀发光的球最好'''
if __name__ == "__main__":

    mybuffer = 64
    pts = deque(maxlen=mybuffer)
    # 打开摄像头
    camera = cv2.VideoCapture(0)
    # 等待两秒
    time.sleep(2)
    while True:
        # 读取帧
        re=re2=0
        re=getcolor(bluLower, bluUpper)
        re2 = getcolor(yelLower, yelUpper)
        if re>re2:
            print 'blue'
        elif re<re2:
            print 'yellow'
        else:
            continue
    # 摄像头释放
    camera.release()
    # 销毁所有窗口
    cv2.destroyAllWindows()
