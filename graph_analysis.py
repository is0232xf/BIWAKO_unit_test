import numpy as np
from matplotlib import pyplot as plt

def return_2d_approx(x, y):
    res = np.polyfit(x, y, 2)
    y2 = np.poly1d(res)(x)
    return res, y2

# raw data
x = np.array([0.0, 0.1, 0.2, 0.25, 0.3])
y = np.array([0.085, 0.18, 0.42, 0.73, 1.15])

# square polyfit
res2=np.polyfit(x, y, 2)
# approximated data
y2 = np.poly1d(res2)(x)

print(res2)

# show the graph
plt.scatter(x, y, label='data')
plt.plot(x, y2)
plt.show()
