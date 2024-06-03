import math
import numpy as np
from PIL import Image
from skimage import draw, io
import matplotlib.pyplot as plt
border = 630
semi_border = border / 2

# 对x坐标转换
def cor_trans_x(cor_l_x):
    add_one(cor_l_x)
    if type(cor_l_x) is list:
        temp = []
        for item in cor_l_x:
            item = round(item)
            if item > 0:
                item += semi_border
                item = abs(item)
            else:
                item += semi_border
            temp.append(item)
    else:
        item = round(cor_l_x)
        item += semi_border
        temp = item
    return temp


# 对y坐标转换
def cor_trans_y(cor_l_y):
    add_one(cor_l_y)
    if type(cor_l_y) is list:
        temp = []
        for item in cor_l_y:
            item = round(item)
            if item > 0:
                item -= semi_border
                item = abs(item)
            else:
                item -= semi_border
                item = abs(item)
            temp.append(item)
    else:
        item = round(cor_l_y)
        item -= semi_border
        item = abs(item)
        temp = item
    return temp


# 解决坐标向下偏移1的问题
def add_one(cor_l_y):
    if type(cor_l_y) is list:
        for i in range(len(cor_l_y)):
            cor_l_y[i] += 1
    else:
        cor_l_y += 1


# 解决面积大一圈的问题
def norm(cor_l):
    def get_max(a):
        if type(a) is list:
            max_c = cor_l[0]
            for item in a:
                if item > max_c:
                    max_c = item
            return max_c
        else:
            max_c = a
            return max_c

    max_C = get_max(cor_l)
    if type(cor_l) is list:
        for i in range(len(cor_l)):
            if cor_l[i] == max_C:
                cor_l[i] -= 1
    else:
        cor_l -= 1


# 读init图片
def read_init(img_name):
    img = io.imread(img_name)
    return img


# 画多边形目标区域
def draw_duo(x, y, img_name):
    color = [255, 255, 0]
    img = io.imread(img_name)
    print(x)
    x = cor_trans_x(x)
    y = cor_trans_y(y)
    norm(x)
    norm(y)
    Y = np.array(y)
    X = np.array(x)
    print(x)
    rr, cc = draw.polygon(Y, X)
    draw.set_color(img, [rr, cc], color)
    # plt.imshow(img, plt.cm.gray)
    return img


# 扣去多边形中间区域
def draw_white(x, y, img_name):
    color = [255, 255, 255]
    img = io.imread(img_name)
    x = cor_trans_x(x)
    y = cor_trans_y(y)
    norm(x)
    norm(y)
    Y = np.array(y)
    X = np.array(x)
    rr, cc = draw.polygon(Y, X)
    draw.set_color(img, [rr, cc], color)
    # plt.imshow(img, plt.cm.gray)
    return img


def draw_round(x, y, R, img_path):
    color = [255, 255, 0]
    img = io.imread(img_path)
    x = cor_trans_x(x)
    y = cor_trans_y(y)
    norm(x)
    norm(y)
    Y = np.array(y)
    X = np.array(x)
    R = round(R)
    rr, cc = draw.circle(X, Y, R)
    draw.set_color(img, [rr, cc], color)
    plt.imshow(img, plt.cm.gray)
    return img


def get_rec_cor(a, b):
    x = [-a, a, a, -a]
    y = [b, b, -b, -b]
    cor = [x[1], y[1]]
    return cor


def draw_rec(x0, y0, a, b, A, img_path):
    X = []
    Y = []

    def get_sym_cor_1(x, y, angle):
        y = 2 * a * math.sin(angle) - y
        x = 2 * a * math.cos(angle) - x
        return x, y

    def get_sym_cor_2(x, y, angle):
        x = 2 * b * math.sin(angle) - x
        y = 2 * b * math.cos(angle) - y
        return x, y

    B = math.atan(b / a)
    C = A + B
    # 矩形斜边long
    long = math.sqrt(a ** 2 + b ** 2)
    y_1 = math.sin(C) * long
    x_1 = math.cos(C) * long
    x_2, y_2 = get_sym_cor_1(x_1, y_1, A)
    x_3, y_3 = -x_1, -y_1
    x_4, y_4 = -x_2, -y_2
    X.append(round(x_1 + x0))
    X.append(round(x_2 + x0))
    X.append(round(x_3 + x0))
    X.append(round(x_4 + x0))
    Y.append(round(y_1 + y0))
    Y.append(round(y_2 + y0))
    Y.append(round(y_3 + y0))
    Y.append(round(y_4 + y0))
    return draw_duo(X, Y, img_path)


# 保存图片
def save(pic):
    io.imsave('init.png', pic)


def show():
    plt.show()


# 获取目标区域面积以及图形矩阵
def get_pic_area(pic):
    img_area = Image.open(pic)
    img_area = img_area.convert('RGB')
    picture_big = np.zeros((border, border))

    def get_area_color(x, y):
        src_list = img_area.load()
        data = src_list[x, y]
        return data

    def get_big_area():
        n = 0
        for i in range(border):
            for j in range(border):
                temp = get_area_color(i, j)
                if temp == (255, 255, 0):
                    n += 1
                    picture_big[i][border - 1 - j] = 1
        return n, picture_big

    area, picture_big = get_big_area()
    print(area)
    return area, picture_big


# 获取图形矩阵的x,y上下界
def get_range(picture_big):
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
    return x_l - semi_border, x_u - semi_border, y_l - semi_border, y_u - semi_border