import math
import multiprocessing
import time
from functools import partial
import random
import numpy as np
from area import area
from draw_init import locate_error, thread_num
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
            x_trans = x_coor + m * CEP * math.sqrt(-2 * math.log(r1)) * math.cos(2 * math.pi * r2) + x_change
            solution.append(x_trans)
        else:
            y_coor = Init_solution[num0]
            y_trans = y_coor + m * CEP * math.sqrt(-2 * math.log(r1)) * math.sin(2 * math.pi * r2) + y_change
            solution.append(y_trans)
    coverageArea = area(small_circles_location=solution)
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
    coverageRatio = np.array(coverageRatio)
    coverageRatio = coverageRatio.flatten().tolist()
    sum0 = 0
    sum1 = 0
    min_area = coverageRatio[0]
    ratio1 = w * 100
    for num in range(len(coverageRatio)):
        sum1 += coverageRatio[num]
        area = coverageRatio[num]
        if area < min_area:
            min_area = area
        if coverageRatio[num] >= ratio1:
            sum0 += 1
    ratiovalue = sum0 / number
    avg = round(sum1 / number, 3)
    min_area = round(min_area, 3)
    time2 = time.time()
    hours, minutes, seconds = c_time(time2 - time1)
    print('平均覆盖面积：', avg, '最小覆盖面积：', min_area)
    print('计算把握程度用时为： ', hours, 'h, ', minutes, 'min ,', seconds, 's')
    return ratiovalue


if __name__ == "__main__":
    xopt1 = [(29.992, 33.812), (-24.471, -55.036), (51.439, 17.551), (37.153, -51.932), (60.639, -15.951), (17.116, -66.217), (-62.721, 5.598), (-16.14, 5.479), (4.233, -15.737), (46.406, 63.786), (-2.203, 60.113), (-41.599, 45.763), (-51.666, -34.69)]
    xopt = []
    for item1, item2 in xopt1:
        xopt.append(item1)
        xopt.append(item2)
    for i in range(20):
        CEP = i + 1
        print('CEP=', CEP)
        print('coverageRatio=',Min_Value(xopt,10000,0.8))
