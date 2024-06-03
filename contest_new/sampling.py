import numpy as np
import random
import math
import time


def get_P_circle(m, r, CEP, times, border):
    def draw_circle_shape(small_r):  # 获取轰炸圆形状
        small_circle_shape = np.zeros((small_r * 2, small_r * 2))
        for x0 in range(0, small_r * 2):
            for y0 in range(0, small_r * 2):
                if (x0 - small_r) ** 2 + (y0 - small_r) ** 2 <= small_r ** 2:
                    small_circle_shape[x0][y0] = 1
        return small_circle_shape

    def f(Init_solution, CEP, m):  # 计算轰炸位置
        solution = []
        for num0 in range(len(Init_solution)):
            r1 = random.random()
            r2 = random.random()
            if (num0 % 2) == 0:
                x_coor = Init_solution[num0]
                x_trans = x_coor + m * CEP * math.sqrt(-2 * math.log(r1)) * math.cos(2 * math.pi * r2)
                solution.append(x_trans)
            else:
                y_coor = Init_solution[num0]
                y_trans = y_coor + m * CEP * math.sqrt(-2 * math.log(r1)) * math.sin(2 * math.pi * r2)
                solution.append(y_trans)
        return solution

    def draw_small_circle(small_circles, small_r, small_circle_shape):  # 计算轰炸概率
        n = 0
        picture_small = np.zeros((border, border))
        circle_num = int(len(small_circles) / 2)
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
                    if 0 <= x < border and 0 <= y < border:  # z
                        if small_circle_shape[x - x_left][y - y_left] == 1:  # A
                            picture_small[x][y] += 1
        return picture_small

    time1 = time.time()
    locations = np.zeros(times + times)
    small_circles_location = f(locations, CEP, m)
    small_circle_shape = draw_circle_shape(r)
    result = draw_small_circle(small_circles_location, r, small_circle_shape)
    f = open('result.txt', 'w')
    for i in range(border):
        for j in range(border):
            result[i][j] = round(result[i][j] / times, 4)
            f.write(str(result[i][j]) + " ")
        f.write("\r\n")
    time2 = time.time()
    print("计算概率圆用时" + str(time2 - time1) + "s")

