# coding=utf-8
import multiprocessing
import time
from area import get_P_num, area
from functools import partial  # 多进程
from cal import c_time, cor_trans
from draw_init import *


def _obj_wrapper(args, kwargs, x):  # 多进程
    return get_P_num(x, *args, **kwargs)


def pso2(l, u, small_num, swarmsize=40, maxiter=100, debug=False):
    time1 = time.time()
    args = ()  # 多进程
    kwargs = {}  # 多进程
    obj = partial(_obj_wrapper, args, kwargs)  # 多进程
    mp_pool = multiprocessing.Pool(thread_num)  # 进程数

    D = small_num * 2  # 小圆个数*2是维度数
    lb = l * np.ones(D)
    ub = u * np.ones(D)
    interval = np.abs(ub - lb)
    vhigh = 0.2 * interval  # 限定
    vlow = -vhigh

    # Initialize objective function
    ite = np.linspace(1, maxiter, maxiter)
    Weight = 0.9 - ite * 0.7 / maxiter
    c1 = 1
    c2 = 1
    x = np.random.rand(swarmsize, D)  # particle positions
    fx = np.zeros(swarmsize)  # current particle function values适应度
    p = np.zeros_like(x)  # best particle positions **pbest**
    fp = np.ones(swarmsize) * 0  # best particle function values **pbest value**
    fg = 0  # best swarm position starting value   **gbest value**

    for i in range(swarmsize):  # particle positions
        for j in range(D):
            x[i][j] = np.random.uniform(lb[j], ub[j])
    fx = np.array(mp_pool.map(obj, x))
    # Initialize the particle's velocity
    v = vlow + np.random.rand(swarmsize, D) * (vhigh - vlow)  # vlow = -vhigh vhigh = np.abs(ub - lb)#限定
    # Calculate objective and constraints for each particle

    for i in range(swarmsize):
        if fx[i] > fp[i]:
            p[i, :] = x[i, :]
            fp[i] = fx[i]
    # Update swarm's best position
    i_max = np.argmax(fp)
    if fp[i_max] > fg:
        fg = fp[i_max]  # best swarm position starting value
        g = p[i_max, :].copy()  # best swarm position
    else:
        g = x[0, :].copy()

    # Iterate until termination criterion met ##################################
    fri_best = np.ones([swarmsize, D])
    for i in range(swarmsize):
        fri_best[i:] = i

    it = 0
    vel = np.zeros_like(v)
    while it <= maxiter - 1:
        for i in range(swarmsize):
            vel[i, :] = Weight[it] * v[i, :] + (c1 * np.random.rand(1, D) * (p[i, :] - x[i, :])) + (
                    c2 * np.random.rand(1, D) * (g - x[i, :]))
        maskl = vel < vlow
        masku = vel > vhigh
        vel = vel * (~np.logical_or(maskl, masku)) + vlow * maskl + vhigh * masku
        pos = x + vel
        x = pos
        v = vel
        # Correct for bound violations限制边界
        maskl = x < lb
        masku = x > ub
        x = x * (~np.logical_or(maskl, masku)) + lb * maskl + ub * masku
        fx = np.array(mp_pool.map(obj, x))
        for i in range(swarmsize):
            if fx[i] > fp[i]:
                p[i, :] = x[i, :]
                fp[i] = fx[i]
        i_max = np.argmax(fp)
        if fp[i_max] > fg:
            g = p[i_max, :].copy()
            fg = fp[i_max]
            if debug:
                print(
                    'New best for swarm at iteration {:}: {:}  目标区域像素点平均覆盖几率为: {:}%'.format(it, cor_trans(small_num, g), fg * 100 / big_area))

        if debug:
            print('Best after iteration {:}: {:}  目标区域像素点平均覆盖几率为: {:}%'.format(it, cor_trans(small_num, g), fg * 100 / big_area))

        it += 1
    time2 = time.time()
    f = area(g)
    print('Stopping search: maximum iterations reached --> {:}'.format(maxiter))
    hours, minutes, seconds = c_time(time2 - time1)
    print('运行时间为： ', hours, 'h, ', minutes, 'min ,', seconds, 's')
    # for num in range(small_num * 2):
    # small_circles[num] = round(small_circles[num])
    # draw_overlap.turtle_overlap((0, 0, int(big_r)), small_r, small_num, g)
    return g, f, fg * 100 / big_area
