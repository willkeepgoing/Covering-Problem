import CoverageRatioWithError as CR

xopt1 = [(4.37, -64.668), (11.713, 29.42), (-5.322, -10.303), (42.991, -43.057), (54.228, -3.716), (51.001, 47.26), (-40.799, -48.563), (-42.609, 35.121), (-60.959, -4.661), (-4.136, 66.091)]

xopt = []
for item1, item2 in xopt1:
    xopt.append(item1)
    xopt.append(item2)
print('把握程度：', CR.Min_Value(xopt, 10000, 0.8))
