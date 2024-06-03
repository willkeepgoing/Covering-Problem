# coding=utf-8
import math
import numpy as np
from PIL import Image
from read_xml import *
from tools import border, semi_border
from sampling import get_P_circle

xml_path = "1.xml"
m = 0.84932180
color = [255, 255, 255]
image = Image.new('RGB', (border, border), (color[0], color[1], color[2]))
image.save("init.png")
pic_path = "init.png"
w1, w2, CEP, small_r, picture_big, big_area = readXML(pic_path, xml_path)
sampling_times = 50000
get_P_circle(m, small_r, CEP, sampling_times, small_r * 4 + 10)
swarmsize = 80
maxiter = 90
debug = True
w1 = [w1]  # 覆盖比例
w2 = [w2]  # 把握程度
l = -border / 2  # 粒子的上下界
u = border / 2
epochs = 10000  # 迭代次数
locate_error = 0
thread_num = 72


def draw_small_circle():
    small_circle_shape = np.zeros((small_r * 2, small_r * 2))
    small = 0  # 加了求小圆的面积
    for x0 in range(0, small_r * 2):
        for y0 in range(0, small_r * 2):
            if (x0 - small_r) ** 2 + (y0 - small_r) ** 2 <= small_r ** 2:
                small_circle_shape[x0][y0] = 1
                small += 1  # 加了求小圆的面积
    return small, small_circle_shape


# small_area, small_circle_shape = draw_small_circle()


# print(big_area)


def init_circle_num():  # 加了个函数
    circles = math.ceil(big_area / small_area)
    print("初始解的个数是：{}".format(circles))
    return circles


def init_big_range():
    semi_border = int(border / 2)
    x_l = y_l = 999
    x_u = y_u = -1
    for x in range(border):
        for y in range(border):
            if picture_big[x][y] == 1:
                if y < y_l:
                    y_l = y
                if y > y_u:
                    y_u = y
                if x < x_l:
                    x_l = x
                if x > x_u:
                    x_u = x
    if y_l < x_l:
        x_l = y_l
    if y_u > x_u:
        x_u = y_u
    return x_l - semi_border, x_u - semi_border


def get_probability_circle():  # 加了个函数
    bor = small_r * 4 + 10
    result = np.zeros((bor, bor))
    f = open('result.txt', 'r')
    i = 0
    line = f.readline()
    while line:
        result[i] = line.split()
        line = f.readline()
        i += 1
    P_2R = result[5:small_r * 4 + 5, 5:small_r * 4 + 5]
    return P_2R


small_area, small_circle_shape = draw_small_circle()
print("使用图片：", pic_path)
l, u = init_big_range()
print("初始化位置上下限：", l, ',', u)
small_num = init_circle_num()
P_circle = get_probability_circle()
# print(small_num)
