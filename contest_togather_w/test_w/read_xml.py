# -*- coding: utf-8 -*-
from xml.dom.minidom import parse
import numpy as np
from PIL import Image
from skimage import draw, io
from tools import draw_round, save, show, draw_duo, draw_white, draw_rec,  get_pic_area, save_one, border


def readXML(pic_path, xml_path):
    domTree = parse(xml_path)
    # 文档根元素
    rootNode = domTree.documentElement
    print("任务编号:", rootNode.getAttribute("任务编号"))
    print("破片面积覆盖比:", rootNode.getAttribute("破片面积覆盖比"))
    w1 = int(rootNode.getAttribute("破片面积覆盖比")[0:len(rootNode.getAttribute("破片面积覆盖比")) - 1])
    w1 /= 100
    w2 = float(rootNode.getAttribute("把握程度"))
    print("把握程度:", rootNode.getAttribute("把握程度"))
    pic = []
    area = []
    zones = rootNode.getElementsByTagName("区域")
    for zone in zones:
        print(zone.nodeName, ":", zone.getAttribute("ID"))
        i = int(zone.getAttribute("ID"))
        color = [255, 255, 255]
        image_one = Image.new('RGB', (border, border), (color[0], color[1], color[2]))
        image_one.save(str(i) + ".png")
        pic_path_one = str(i) + ".png"
        print("形状:", zone.getAttribute("形状"))
        if zone.getAttribute("形状") == "多边形":
            outline1 = zone.getElementsByTagName("轮廓")[0]
            points1 = outline1.getElementsByTagName("角点")
            X1 = np.empty(0)
            Y1 = np.empty(0)
            for point in points1:
                X1 = np.append(X1, int(point.getAttribute("X")))
                Y1 = np.append(Y1, int(point.getAttribute("Y")))
            print("X1:", X1)
            print("Y1:", Y1)
            save_one(draw_duo(X1.tolist(), Y1.tolist(), pic_path_one), i)
            save(draw_duo(X1.tolist(), Y1.tolist(), pic_path))
            times = 1
            while zone.getElementsByTagName("轮廓").length > times:
                outline2 = zone.getElementsByTagName("轮廓")[times]
                points2 = outline2.getElementsByTagName("角点")
                X2 = np.empty(0)
                Y2 = np.empty(0)
                for point in points2:
                    X2 = np.append(X2, int(point.getAttribute("X")))
                    Y2 = np.append(Y2, int(point.getAttribute("Y")))
                print("X2:", X2)
                print("Y2:", Y2)
                save_one(draw_white(X2.tolist(), Y2.tolist(), pic_path_one), i)
                save(draw_white(X2.tolist(), Y2.tolist(), pic_path))
                times += 1

        elif zone.getAttribute("形状") == "圆形":
            point = zone.getElementsByTagName("中心点")[0]
            X = int(point.getAttribute("X"))
            Y = int(point.getAttribute("Y"))
            r_round = zone.getElementsByTagName("半径")[0]
            R = int(r_round.getAttribute("R"))
            print("X:", str(X))
            print("Y:", str(Y))
            print("半径:", str(R))
            save_one(draw_round(X, Y, R, pic_path_one), i)
            save(draw_round(X, Y, R, pic_path))
        elif zone.getAttribute("形状") == "矩形":
            point = zone.getElementsByTagName("中心点")[0]
            X = int(point.getAttribute("X"))
            Y = int(point.getAttribute("Y"))
            print("X:", str(X))
            print("Y:", str(Y))
            length = zone.getElementsByTagName("长度")[0]
            l = int(length.getAttribute("L"))
            print("长度:", str(l))
            width = zone.getElementsByTagName("宽度")[0]
            w = int(width.getAttribute("W"))
            print("宽度:", str(w))
            arc = zone.getElementsByTagName("长轴与X轴夹角")[0]
            a = float(arc.getAttribute("A"))
            print("长轴与X轴夹角:", str(a))
            save_one(draw_rec(X, Y, l / 2, w / 2, a, pic_path_one), i)
            save(draw_rec(X, Y, l / 2, w / 2, a, pic_path))

        a_area, a_pic = get_pic_area(pic_path_one)
        pic.append(a_pic)
        area.append(a_area)


    WQ = rootNode.getElementsByTagName("破片战斗部")[0]
    print("CEP:", WQ.getAttribute("CEP"))
    print("破片有效杀伤半径:", WQ.getAttribute("破片有效杀伤半径"))
    CEP = round(float(WQ.getAttribute("CEP")))
    r = int(WQ.getAttribute("破片有效杀伤半径"))
    all_area, all_pic = get_pic_area(pic_path)
    pic.insert(0, all_pic)
    area.insert(0, all_area)
    # 将图片转换为矩阵(pic_path转换为pic)
    print("area:")
    print(area)
    return w1, w2, CEP, r, pic, area


if __name__ == '__main__':
    border = 630
    color = [255, 255, 255]
    image = Image.new('RGB', (border, border), (color[0], color[1], color[2]))
    image.save("init.png")
    pic_path = "init.png"
    w1, w2, CEP, r, pic = readXML(pic_path)
    print(w1)
    print(w2)
    print(CEP)
    print(r)
    print(pic)
