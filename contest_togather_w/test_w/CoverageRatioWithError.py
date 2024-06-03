import multiprocessing
import time
from functools import partial
import numpy as np
import random
import math
from area import *
from draw_init import *
from cal import c_time
m = 0.84932180  # 坐标变换时的系数
# m = 1.17741002  # 坐标变换时的系数


def _obj_wrapper0(args, kwargs, x):  # 多进程
    return func0(x, *args, **kwargs)


def func0(Init_solution):
    solution = []
    # 定位误差
    length = random.randint(0, locate_error)
    x_change = random.randint(int(np.ceil(-length)), int(np.floor(length)))
    y_1 = [int(np.floor(math.sqrt(length ** 2 - x_change ** 2))),
          int(np.ceil(-math.sqrt(length ** 2 - x_change ** 2)))]
    y_change = random.choice(y_1)
    coverageRatio = []

    for num0 in range(len(Init_solution)):
        r1 = random.random()
        r2 = random.random()
        if (num0 % 2) == 0:
            x_coor = Init_solution[num0]
            x_trans = x_coor + m * CEP * math.sqrt(-2 *math.log(r1)) * math.cos(2 * math.pi * r2) + x_change
            solution.append(x_trans)
        else:
            y_coor = Init_solution[num0]
            y_trans = y_coor + m * CEP * math.sqrt(-2 *math.log(r1)) * math.sin(2 * math.pi * r2) + y_change
            solution.append(y_trans)
    coverageArea = area(small_circles_location=solution + [0])
    coverageRatio.append(coverageArea)
    return coverageRatio


# 在考虑误差的情况下，满足把握条件实际所需的最小的覆盖比例
def Min_Value(Init_solution, number, w):
    time1 = time.time()
    args = ()  # 多进程
    kwargs = {}  # 多进程
    mp_pool = multiprocessing.Pool(thread_num)  # 进程数
    obj = partial(_obj_wrapper0, args, kwargs)  # 多进程
    x = np.random.rand(number, len(Init_solution))
    for i in range(number):
        x[i] = Init_solution
    coverageRatio = np.array(mp_pool.map(obj, x))
    ratio1 = w * 100
    ratiovalue = []
    togather_w = [0] * number
    sum_togather = 0
    for pic in range(len(big_area)):
        sum0 = 0
        sum1 = 0
        for num in range(len(coverageRatio)):
            sum1 += coverageRatio[num][0][pic]
            if coverageRatio[num][0][pic] >= ratio1:
                togather_w[num] += 1
                sum0 += 1
        ratiovalue.append(sum0 / number)
        avg = round(sum1 / number, 3)
        print('图形：', pic, '的平均覆盖比例：', avg)

    for epoch in range(number):
        if togather_w[epoch] == len(big_area):
            sum_togather += 1

    time2 = time.time()
    hours, minutes, seconds = c_time(time2 - time1)
    print('计算把握程度用时为： ', hours, 'h, ', minutes, 'min ,', seconds, 's')

    return ratiovalue, sum_togather / number


def located_error():  # 保留了小数点后五位
    r1 = random.randint(1, 999) / 1000
    r2 = random.randint(1, 999) / 1000
    error_x = round(5 * (-2 * math.log(r1)) ** 0.5 * math.cos(2 * math.pi * r2), 5)
    error_y = round(5 * (-2 * math.log(r1)) ** 0.5 * math.sin(2 * math.pi * r2), 5)
    print("定位误差为(" + str(error_x) + ", " + str(error_y) + ")")
    return error_x, error_y


if __name__ == '__main__':
    #print(Min_Value([43.0, 44.0, 39.0, 47.0, -19.0, 9.0, -20.0, 9.0, 39.0, 44.0, 7.0, 5.0, 25.0, -4.0, 43.0, 42.0, 19.0, -1.0, -21.0, 12.0, 41.0, 45.0, 46.0, 45.0, 25.0, -1.0, -15.0, 9.0, 40.0, 37.0, 16.0, -2.0, -4.0, 9.0], 10000, 0.8))
    #print(Min_Value([43.0, 44.0, 39.0, 47.0, -19.0, 9.0, -20.0, 9.0, 39.0, 44.0, 7.0, 5.0, 25.0, -4.0, 43.0, 42.0, 19.0, -1.0, -21.0, 12.0, 41.0, 45.0, 46.0, 45.0, 25.0, -1.0, -15.0, 9.0, 40.0, 37.0, 16.0, -2.0, -4.0, 9.0], 10000, 0.8))
    #print(Min_Value([43.0, 44.0, 39.0, 47.0, -19.0, 9.0, -20.0, 9.0, 39.0, 44.0, 7.0, 5.0, 25.0, -4.0, 43.0, 42.0, 19.0, -1.0, -21.0, 12.0, 41.0, 45.0, 46.0, 45.0, 25.0, -1.0, -15.0, 9.0, 40.0, 37.0, 16.0, -2.0, -4.0, 9.0], 10000, 0.8))
    #print(Min_Value([43.0, 44.0, 39.0, 47.0, -19.0, 9.0, -20.0, 9.0, 39.0, 44.0, 7.0, 5.0, 25.0, -4.0, 43.0, 42.0, 19.0, -1.0, -21.0, 12.0, 41.0, 45.0, 46.0, 45.0, 25.0, -1.0, -15.0, 9.0, 40.0, 37.0, 16.0, -2.0, -4.0, 9.0], 10000, 0.8))
    #print(Min_Value([43.0, 44.0, 39.0, 47.0, -19.0, 9.0, -20.0, 9.0, 39.0, 44.0, 7.0, 5.0, 25.0, -4.0, 43.0, 42.0, 19.0, -1.0, -21.0, 12.0, 41.0, 45.0, 46.0, 45.0, 25.0, -1.0, -15.0, 9.0, 40.0, 37.0, 16.0, -2.0, -4.0, 9.0], 10000, 0.8))
    # print(Min_Value([88.0, -27.0, 90.0, -25.0, 62.0, -33.0, 33.0, -28.0, 34.0, -30.0], 100000, 0.8))
    for i in range(1000):
        located_error()