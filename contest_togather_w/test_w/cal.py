def c_time(time_long):
    seconds = time_long % 60
    time_long = time_long - seconds
    # print('seconds: ', seconds)
    time_long = int(time_long / 60)
    minutes = time_long % 60
    # print('minutes: ', minutes)
    hours = int(time_long / 60)
    # print('hours: ', hours)
    return hours, minutes, seconds


def cor_trans(num, xopt):
    temp = []
    for i in range(num):
        temp_small = (round(xopt[i * 2], 3), round(xopt[i * 2 + 1], 3))
        temp.append(temp_small)
    return temp


if __name__ == '__main__':
    time = 20000
    print(c_time(time))
    print(int(5 / 2))
    a = 1.12313
    b = 1231241.123
    c = []
    temp = (a, b)
    c.append(temp)

    print(c)
    xopt = [285.79440012, 37.77890223, -105.98002674, 3.07580056, 69.85326428,
            -279.05768939, 153.18303864, 41.90733325, -40.89577789, 137.60652013, 31.28444144, 3.41349183]
    temp = cor_trans(6, xopt)
    print(temp)

