import matplotlib.pyplot as plt
import numpy as np
from skimage import draw
from tools import add_one
import matplotlib.image as mp
from draw_init import small_r, border, locate_error, CEP
import area
import math
import random
import time
import os

m = 0.84932180
circle_r = small_r
semi_border = int(border / 2)


def cor_trans(circles_location):
    for i in range(len(circles_location)):
        if i % 2 == 1:
            circles_location[i] = cor_trans_y(circles_location[i])
        else:
            circles_location[i] = cor_trans_x(circles_location[i])

# 对x坐标转换
def cor_trans_x(cor_l_x):
    add_one(cor_l_x)
    item = round(cor_l_x)
    if item > 0:
        item += semi_border
        item = abs(item)
    else:
        item += semi_border
    return item


# 对y坐标转换
def cor_trans_y(cor_l_y):
    add_one(cor_l_y)
    item = round(cor_l_y)
    if item > 0:
        item -= semi_border
        item = abs(item)
    else:
        item -= semi_border
        item = abs(item)
    return item


def draw_pic(circles_location, flag, image_path, fgbl, bwcd):
    color = [255, 0, 0]

    if flag == 1:
        circle_sum = int(len(circles_location) / 2)
        img = mp.imread(image_path)
        np.array(img, np.int32)
        # if a >= 80:
            #  j += 1
        plt.title('FUGAIBILI: ' + str(fgbl) + '%, BAWOCHENGDU: ' + str(bwcd) + '%')
        dir = os.getcwd()
        pic_dir = os.path.join(dir, 'picture')
        if os.path.exists(pic_dir):
            os.listdir(pic_dir)
        else:
            os.mkdir(pic_dir)
        all_pic = os.listdir(pic_dir)
        if all_pic == []:
            num = 0
        else:
            l_pic = all_pic[-1]
            num , _ = os.path.splitext(l_pic)
        pic_name = str(int(num) + 1) + '.png'
        pic_path = os.path.join(pic_dir, pic_name)
        cor_trans(circles_location)
        for current in range(circle_sum):
            rr, cc = draw.circle_perimeter(round(circles_location[current * 2]), round(circles_location[current * 2 + 1]), circle_r)
            draw.set_color(img, [cc, rr], color=color)
            plt.imshow((img * 255).astype(np.uint8))
            img = np.clip(img, 0.0, 1.0)
        mp.imsave(pic_path, img)
    if flag == 2:
        img = np.clip(img, 0.0, 1.0)
        out_path = 'picture/' + str(num) + '.png'
        mp.imsave(out_path, img)


if __name__ == "__main__":
    xopt = [-4.974, 55.015, -51.152, 39.861, 7.262, -57.164, 14.845, -0.792, -13.689, -0.583, 37.674, 48.761, 53.493,
            -42.248, 59.589, 7.507, -60.538, -9.909, -35.673, -49.623]
    draw_pic(xopt, 1, 'round/round_80.png', 10)
