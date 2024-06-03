# coding=utf-8
import time
from draw import draw_pic
import CoverageRatioWithError as CR
import area
import cal
from PSO import pso
from PSO2 import pso2
from draw_init import *
from write_xml import write_xml

for w in w1:
    time1 = time.time()
    id_num = len(big_area)
    num = 1  # 条件下整体循环的次数
    xopt1, fopt1 = pso(l, u, small_num, swarmsize=swarmsize, maxiter=maxiter, debug=debug)
    coveragevalue, togather_w = CR.Min_Value(xopt1, epochs, w)
    print('第', num, '轮计算结果')
    print("小圆的个数为：{}".format(small_num))
    cir = cal.cor_trans(small_num, xopt1)
    print("小圆的圆心坐标为：{}".format(cir))
    print("覆盖比例为{}".format(fopt1))
    print("把握程度为：{}".format(coveragevalue))
    print("同时把握程度为：{}".format(togather_w))
    for ww in w2:
        while fopt1 < w or togather_w < ww:
            small_num += 1
            num += 1
            xopt1, fopt1, f_num = pso2(l, u, small_num, swarmsize=swarmsize, maxiter=maxiter, debug=debug)
            coveragevalue, togather_w = CR.Min_Value(xopt1, epochs, w)
            print('第', num, '轮计算结果')
            print("小圆的个数为：{}".format(small_num))
            cir = cal.cor_trans(small_num, xopt1)
            print("小圆的圆心坐标为：{}".format(cir))
            print("目标区域像素点平均覆盖几率为{}".format(f_num))
            print("把握程度为：{}".format(coveragevalue))
            print("同时把握程度为：{}".format(togather_w))
        # 第一步检测
        fopt1 = area.area(xopt1)
        print('开始第一步检测...')
        small_num = int(len(xopt1) / 2)
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
            current_coveragevalue, current_togather_w = CR.Min_Value(xopt2, epochs, w)
            print('第一步检测中的把握程度: ', current_coveragevalue)
            print('第一步检测中的同时把握程度: ', current_togather_w)
            if current_togather_w >= ww:
                if small_num == 0:
                    break
                fopt1 = current_area
                coveragevalue = current_coveragevalue
                togather_w = current_togather_w
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
            current_coveragevalue, current_togather_w = CR.Min_Value(max_xopt2, epochs, w)
            print('第二次检测中的把握程度: ', current_coveragevalue)
            print('第二次检测中的同时把握程度: ', current_togather_w)
            if current_togather_w < ww:
                print("处理后的覆盖比:{}".format(fopt1))
                print("处理后的把握程度:{}".format(coveragevalue))
                print("处理后的同时把握程度:{}".format(togather_w))
                print("小圆的半径R为{}".format(small_r),
                      "CEP为{}".format(CEP), "覆盖比例为{}".format(w), "最小把握程度为{}".format(ww))
                print("最优解对应的小圆的个数为：{}".format(small_num))
                big = cal.cor_trans(small_num, xopt1)
                print("最优解对应的小圆的圆心坐标为：{}".format(big))
                print("模拟次数为:{}".format(num))
                mean_p = area.get_P_num(xopt1)
                print("目标区域像素点平均覆盖几率为{}".format(mean_p * 100 / big_area[0]))
                f = open("P.txt", "w")
                r = area.get_P_result(xopt1)
                for i in range(border):
                    for j in range(border):
                        f.write(str(r[i][j]) + " ")
                    f.write("\r\n")
                f.close()
                break
            else:
                if small_num < 2 :
                    print("处理后的覆盖比:{}".format(fopt1))
                    print("处理后的把握程度:{}".format(coveragevalue))
                    print("处理后的同时把握程度:{}".format(togather_w))
                    print("小圆的半径R为{}".format(small_r), "CEP为{}".format(CEP), "覆盖比例为{}".format(w), "最小把握程度为{}".format(ww))
                    print("最优解对应的小圆的个数为：{}".format(small_num))
                    big = cal.cor_trans(small_num, max_xopt2)
                    xopt1 = max_xopt2
                    print("最优解对应的小圆的圆心坐标为：{}".format(big))
                    print("模拟次数为:{}".format(num))
                    mean_p = area.get_P_num(xopt1)
                    print("目标区域像素点平均覆盖几率为{}".format(mean_p * 100 / big_area[0]))
                    f = open("P.txt", "w")
                    r = area.get_P_result(xopt1)
                    for i in range(border):
                        for j in range(border):
                            f.write(str(r[i][j]) + " ")
                        f.write("\r\n")
                    f.close()
                    break
                fopt1 = max_area
                coveragevalue = current_coveragevalue
                togather_w = current_togather_w
                xopt1 = max_xopt2
                small_num = int(len(xopt1) / 2)
                print('small_num: ', small_num)
                max_area = 0
                xopt1 = max_xopt2
        time2 = time.time()
        hours, minutes, seconds = cal.c_time(time2 - time1)
        print('运行时间为： ', hours, 'h, ', minutes, 'min ,', seconds, 's')
        draw_pic(xopt1, 1, pic_path, fopt1, coveragevalue[0])
        write_xml(big)
        print('画图完成')
