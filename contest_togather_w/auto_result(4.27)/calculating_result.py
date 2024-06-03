import math
import numpy as np
import time


def calculating_one_point_1(CEP, r, dis_to_center, w_angel, m):  # 计算某一点在某一方向上被覆盖的几率
    w_angel = math.pi / 2 - w_angel  # 第一象限
    if r < (dis_to_center * math.sin(w_angel)):
        return 0
    else:
        d_max = dis_to_center * math.cos(w_angel) + math.sqrt(r * r - (dis_to_center * math.sin(w_angel)) ** 2)
        d_min = 0
        if dis_to_center > r:
            d_min = 2 * dis_to_center * math.cos(w_angel) - d_max
        r1 = math.e ** (-(d_max / (m * CEP)) ** 2 / 2)
        r1_ = math.e ** (-(d_min / (m * CEP)) ** 2 / 2)
        return r1_ - r1


def calculating_one_point_4(CEP, r, dis_to_center, w_angel, m):  # 计算某一点在某一方向上被覆盖的几率
    w_angel = math.pi / 2 + w_angel  # 第一象限
    if r < (dis_to_center * math.sin(w_angel)):
        return 0
    else:
        d_max = math.sqrt(r * r - (dis_to_center * math.sin(w_angel)) ** 2) - dis_to_center * math.cos(w_angel)
        r1 = math.e ** (-(d_max / (m * CEP)) ** 2 / 2)
        return 1 - r1


def calculating_all(angel_sum, direction_1, direction_4, CEP, r, m):  # 计算某一点在某一方向上被覆盖的几率
    size = 4 * r + 1
    bisize = (int)(size / 2)
    result = np.zeros([size, size])
    for i in range(bisize + 1):
        for j in range(bisize + 1):
            avg = 0
            distance = math.sqrt((bisize - i) ** 2 + (bisize - j) ** 2)
            for k in direction_1:
                avg += round(calculating_one_point_1(CEP, r, distance, k, m), 5)
            for k in direction_4:
                if distance > r:
                    break
                avg += round(calculating_one_point_4(CEP, r, distance, k, m), 5)
            avg /= angel_sum
            # print(avg)
            avg = round(avg, 5)
            result[i][j] = result[size - i - 1][j] = result[i][size - j - 1] = result[size - i - 1][size - j - 1] = avg
    f = open("P_circle.txt", "w")
    for i in range(size):
        for j in range(size):
            f.write(str(result[i][j]) + " ")
        f.write("\r\n")
    f.close()
    return result


def get_P_circle(m, CEP, r):
    time1 = time.time()
    angel_sum = 180
    direction_1 = np.linspace(0, math.pi / 2, (int)(angel_sum / 2))  # 第一象限所有角度
    direction_4 = np.linspace(-math.pi / 2, 0, (int)(angel_sum / 2))  # 第一象限所有角度
    result = calculating_all(angel_sum, direction_1, direction_4, CEP, r, m)
    time2 = time.time()
    # print(time2 - time1)  # 131 * 131,也就是运行时间r为30的圆，0.5s计算完成
    return result

if __name__ == '__main__':
    CEP = 20
    r = 30
    m = 0.84932180
    result = get_P_circle(m, CEP, r)