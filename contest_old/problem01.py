# coding=utf-8

import time
from draw import *
import CoverageRatioWithError as CR
import area
import cal
from PSO import pso
from draw_init import *
from write_xml import write_xml

for w in w1:
    time1 = time.time()
    num = 1  # 条件下整体循环的次数
    xopt1, fopt1 = pso(l, u, small_num, swarmsize=swarmsize, maxiter=maxiter, debug=debug)
    coveragevalue = CR.Min_Value(xopt1, epochs, w)
    print('第', num, '轮计算结果')
    print("小圆的个数为：{}".format(small_num))
    cir = cal.cor_trans(small_num, xopt1)
    print("小圆的圆心坐标为：{}".format(cir))
    print("覆盖比例为{}".format(fopt1))
    print("把握程度为：{}".format(coveragevalue))
    for ww in w2:
        while fopt1 < w or coveragevalue < ww:
            small_num += 1
            num += 1
            xopt1, fopt1 = pso(l, u, small_num, swarmsize=swarmsize, maxiter=maxiter, debug=debug)
            coveragevalue = CR.Min_Value(xopt1, epochs, w)
            print('第', num, '轮计算结果')
            print("小圆的个数为：{}".format(small_num))
            cir = cal.cor_trans(small_num, xopt1)
            print("小圆的圆心坐标为：{}".format(cir))
            print("覆盖比例为{}".format(fopt1))
            print("把握程度为：{}".format(coveragevalue))
        # 第一步检测
        print('开始第一步检测...')
        print("第一步轮检测前的把握程度和检测前小圆的个数: ", coveragevalue, small_num)
        print("第一步检测前的最好覆盖比例: ", fopt1)
        small_temp = cal.cor_trans(small_num, xopt1)
        print("第一步检测前的小圆坐标: ", small_temp)
        current_area = fopt1

        useless_mini_ciecles = area.first_check(xopt1, small_num, current_area, w)
        # first_delete_mini_circles_num = int(len(useless_mini_ciecles))
        deleted = 0
        for delete_mini_circle in useless_mini_ciecles:
            index = [delete_mini_circle[0] - deleted, delete_mini_circle[1] - deleted]
            xopt2 = np.delete(xopt1, index)
            current_coveragevalue = CR.Min_Value(xopt2, epochs, w)
            print('第一步检测current_coveragevalue: ', current_coveragevalue)
            if current_coveragevalue >= ww:
                if small_num == 0:
                    break
                fopt1 = current_area
                coveragevalue = current_coveragevalue
                xopt1 = xopt2
                small_num = int(len(xopt1) / 2)
                print('small_num: ', small_num)
                deleted += 2

        # 第二步检测
        print('开始第二步检测...')
        print("第二步检测前的把握程度和检测前小圆的个数: ", coveragevalue, small_num)
        print("第二步检测前的最好覆盖比例: ", fopt1)
        small_temp = cal.cor_trans(small_num, xopt1)
        print("第二步检测前的小圆坐标: ", small_temp)
        small_num = int(len(xopt1) / 2)
        max_xopt2 = xopt1
        current_area = fopt1
        max_area = 0

        while True:
            max_xopt2, max_area = area.second_check(xopt1, small_num, max_area)
            current_coveragevalue = CR.Min_Value(max_xopt2, epochs, w)
            print('current_coveragevalue: ', current_coveragevalue)
            if current_coveragevalue < ww:
                print("处理后的覆盖比:{}".format(fopt1))
                print("处理后的把握程度:{}".format(coveragevalue))
                print("小圆的半径R为{}".format(small_r), "CEP为{}".format(CEP), "覆盖比例为{}".format(w), "把握程度为{}".format(ww))
                print("最优解对应的小圆的个数为：{}".format(small_num))
                big = cal.cor_trans(small_num, xopt1)
                print("最优解对应的小圆的圆心坐标为：{}".format(big))
                print("模拟次数为:{}".format(num))
                break
            else:
                if small_num == 0:
                    break
                fopt1 = max_area
                coveragevalue = current_coveragevalue
                xopt1 = max_xopt2
                small_num = int(len(xopt1) / 2)
                print('small_num: ', small_num)
                max_area = 0
                xopt1 = max_xopt2
        time2 = time.time()
        hours, minutes, seconds = cal.c_time(time2 - time1)
        print('运行时间为： ', hours, 'h, ', minutes, 'min ,', seconds, 's')
        draw_pic(xopt1, 1, pic_path, fopt1, coveragevalue)
        write_xml(big)
        print('画图完成')
