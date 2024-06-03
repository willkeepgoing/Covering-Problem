# coding=utf-8
import numpy as np
from draw_init import *


def area(small_circles_location):
    # small_circles_location = prep(small_circles_location)
    # print('small_circles_location: ', small_circles_location)
    circle_num = int(len(small_circles_location) / 2)
    # print('circle_num: ', circle_num)
    
    def draw_small_circle(small_circles):
        n = 0
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
                    if 0 <= x < border and 0 <= y < border:  # z����
                        if small_circle_shape[x - x_left][y - y_left] == 1:  # A����
                            if picture_small[x][y] == 0 and picture_big[x][y] == 1:
                                picture_small[x][y] = 1
                                n += 1
        return n

    picture_small = np.zeros((border, border))
    count_area = draw_small_circle(small_circles_location)
    return count_area / big_area * 100


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
#
# if __name__ == "__main__":
#     print(area([220, 200, 0, 0, 180, 180, -200, -220]))
