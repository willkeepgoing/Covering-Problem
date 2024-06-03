# coding=utf-8
import numpy as np
from draw_init import *
from cal import c_time
import time


def area(small_circles_location):

    def draw_small_circle(small_circles, pic):
        n = 0
        picture_small = np.zeros((border, border))
        for num0 in range(circle_num * 2):
            small_circles[num0] = round(small_circles[num0])
        semi_border = int(border / 2)
        for circles_num in range(circle_num):
            x_left = int(small_circles[circles_num * 2] - small_r + semi_border)
            x_right = int(small_circles[circles_num * 2] + small_r + semi_border)
            y_left = int(small_circles[circles_num * 2 + 1] - small_r + semi_border)
            y_right = int(small_circles[circles_num * 2 + 1] + small_r + semi_border)
            for x in range(x_left, x_right):
                for y in range(y_left, y_right):
                    if 0 <= x < border and 0 <= y < border:
                        if small_circle_shape[x - x_left][y - y_left] == 1:
                            if picture_small[x][y] == 0 and picture_big[pic][x][y] == 1:
                                picture_small[x][y] = 1
                                n += 1
        return n / big_area[pic] * 100

    circle_num = int(len(small_circles_location) / 2)
    if len(small_circles_location) % 2 == 0:
        id = 0
        count_area = draw_small_circle(small_circles_location, id)
    else:
        count_area = []
        for id in range(len(picture_big)):
            count_area.append(draw_small_circle(small_circles_location, id))
    return count_area


def first_check(xopt1, mini_num, start_area, w):
    print("第一步遍历删去圆之前的坐标为：{}".format(xopt1))
    useless_min_circle = []
    for mini_circles_num in range(mini_num):
        index = [mini_circles_num * 2, mini_circles_num * 2 + 1]
        xopt2 = np.delete(xopt1, index)
        # print('xopt2', xopt2)
        current_area = area(xopt2)
        # print('current_area', current_area)
        # print('max_area', max_area)
        if start_area - current_area < 0.001 and current_area > w:
            useless_min_circle.append(index)
    # print("第一步遍历得到的无关圆的坐标为：{}".format(useless_min_circle))
    print("第一步遍历得到的无关圆个数为：{}".format(len(useless_min_circle)))
    return useless_min_circle


def second_check(xopt1, mini_num, max_area):
    print("第二步遍历删去圆之前的坐标为：{}".format(xopt1))
    max_xopt2 = xopt1
    for mini_circles_num in range(mini_num):
        index = [mini_circles_num * 2, mini_circles_num * 2 + 1]
        xopt2 = np.delete(xopt1, index)
        # print('xopt2', xopt2)
        current_area = area(xopt2)
        # print('current_area', current_area)
        # print('max_area', max_area)
        if current_area > max_area:
            max_area = current_area
            max_xopt2 = xopt2
    print("第二步遍历删去圆之后的坐标为：{}".format(max_xopt2))
    return max_xopt2, max_area


def prep(locations):
    circle_num = int(len(locations) / 2)
    t_locations = []
    for i in range(circle_num):
        if (locations[i * 2] - 0) ** 2 + (locations[i * 2 + 1] - 0) ** 2 <= r ** 2:
            t_locations.append(int(round(locations[i * 2])))
            t_locations.append(int(round(locations[i * 2 + 1])))
    return t_locations


def get_P_num(small_circles):  # 计算平均覆盖几率大于w的像素点数量
    r = 0
    # P_circle 概率圆矩阵 [0 : 120][0 : 120]
    picture_P = np.ones((border, border))
    circle_num = int(len(small_circles) / 2)
    for num0 in range(circle_num * 2):
        small_circles[num0] = round(small_circles[num0])
    semi_border = int(border / 2)
    rr = small_r * 2
    for circles_num in range(circle_num):
        x_left = int(small_circles[circles_num * 2] - rr + semi_border)
        x_right = int(small_circles[circles_num * 2] + rr + semi_border)
        y_left = int(small_circles[circles_num * 2 + 1] - rr + semi_border)
        y_right = int(small_circles[circles_num * 2 + 1] + rr + semi_border)
        for x in range(max(x_left, 0), min(x_right, border)):
            for y in range(max(y_left, 0), min(y_right, border)):
                picture_P[x][y] *= 1 - P_circle[x - x_left][y - y_left]
    for i in range(border):
        for j in range(border):
            if picture_big[0][i][j] == 1:
                r += 1 - picture_P[i][j]
    return r


def get_P_result(small_circles):  # 平均覆盖几率矩阵的的计算
    w = 1 - w2[0]
    print("大小:")
    print(P_circle.size)
    # P_circle 概率圆矩阵 [0 : 120][0 : 120]
    picture_P = np.ones((border, border))
    circle_num = int(len(small_circles) / 2)
    for num0 in range(circle_num * 2):
        small_circles[num0] = round(small_circles[num0])
    semi_border = int(border / 2)
    rr = small_r * 2
    for circles_num in range(circle_num):
        x_left = int(small_circles[circles_num * 2] - rr + semi_border)
        x_right = int(small_circles[circles_num * 2] + rr + semi_border)
        y_left = int(small_circles[circles_num * 2 + 1] - rr + semi_border)
        y_right = int(small_circles[circles_num * 2 + 1] + rr + semi_border)
        for x in range(max(x_left, 0), min(x_right, border)):
            for y in range(max(y_left, 0), min(y_right, border)):
                picture_P[x][y] *= 1 - P_circle[x - x_left][y - y_left]
    for i in range(border):
        for j in range(border):
            if picture_big[0][i][j] == 0:
                picture_P[i][j] = -1
            else:
                picture_P[i][j] = 1 - picture_P[i][j]

    return picture_P
# if __name__ == "__main__":
#     print(area([220, 200, 0, 0, 180, 180, -200, -220]))
