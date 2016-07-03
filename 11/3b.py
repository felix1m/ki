import numpy as np
k = [[0.075, 0.124, 0.075],
        [0.124, 0.204, 0.124],
        [0.075, 0.124, 0.075]]

p1 = [[184, 120, 72],
      [60, 140, 64],
      [128, 112, 96]]


p2 = [[120, 72, 56],
      [140, 64, 60],
      [112, 96, 64]]

res1 = np.array(k) * np.array(p1)
print(res1.sum(axis=0).sum(axis=0))
res2 = np.array(k) * np.array(p2)
print(res2.sum(axis=0).sum(axis=0))

p3 = [[128, 112, 96],
      [120, 102, 96],
      [120, 102, 96]]

res3 = np.array(k) * np.array(p3)
print(res3.sum(axis=0).sum(axis=0))
