import numpy as np
import matplotlib.pyplot as plt

scale = 100
n = 1000
x = scale*(np.random.random_sample((n,))-0.5)
y = scale*(np.random.random_sample((n,))-0.5)
# x = np.arange(0, 5, 0.5);
# y = np.sin(x)
plt.plot(x, y, 'ro', label='random data')
# y = np.cos(x)
# plt.plot(x, y, 'g-', label='cos data')
plt.legend()
plt.savefig('../data/sin.png')