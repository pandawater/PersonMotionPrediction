import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
# 假设您有一个包含准确率的数组 accuracy_values，其中每个元素对应一个 epoch 的准确率值
holdthigh= [0.117, 0.238, 0.371, 0.538, 0.717, 0.909, 1.117, 1.348, 1.592, 1.850,
              2.134, 2.432, 2.740, 3.057, 3.373, 3.703, 4.036, 4.376, 4.703, 5.043,
              5.386, 5.737, 6.074, 6.421, 6.765, 7.115, 7.441, 7.775, 8.108, 8.451]


cpr = [0.121, 0.238, 0.361, 0.505, 0.660, 0.820, 0.987, 1.169, 1.359, 1.563,
              1.786, 2.015, 2.243, 2.481, 2.723, 2.975, 3.227, 3.489, 3.744, 4.007,
              4.271, 4.540, 4.800, 5.071, 5.341, 5.622, 5.899, 6.187, 6.474, 6.769]

sc =[0.084, 0.162, 0.246, 0.341, 0.448, 0.564, 0.687, 0.819, 0.963, 1.115,
              1.281, 1.454, 1.633, 1.821, 2.015, 2.215, 2.422, 2.631, 2.836, 3.047,
              3.260, 3.477, 3.694, 3.913, 4.133, 4.356, 4.578, 4.803, 5.028, 5.257]



armwrestle = [0.080, 0.155, 0.234, 0.327, 0.437, 0.555, 0.683, 0.818, 0.962, 1.114,
              1.277, 1.443, 1.612, 1.788, 1.968, 2.155, 2.343, 2.534, 2.726, 2.923,
              3.122, 3.324, 3.526, 3.729, 3.932, 4.137, 4.338, 4.541, 4.742, 4.947]

judo = [0.092, 0.182, 0.278, 0.392, 0.518, 0.652, 0.796, 0.952, 1.115, 1.288,
              1.479, 1.677, 1.883, 2.095, 2.308, 2.529, 2.753, 2.983, 3.212, 3.447,
              3.688, 3.931, 4.167, 4.409, 4.653, 4.901, 5.141, 5.387, 5.635, 5.887]


# 创建一个包含 epoch 数的数组
epoch_interval = 1
epochs = list(range(0, 2 * epoch_interval, epoch_interval))



# 绘制训练损失图
plt.plot(epochs, holdthigh[0:2], label='holdthigh')
plt.plot(epochs, cpr[0:2], label='cpr')
plt.plot(epochs, sc[0:2], label='security check')
plt.plot(epochs, armwrestle[0:2], label='arm wrestle')
plt.plot(epochs, judo[0:2], label='judo hold')
plt.title('JME Error with Frame Number')
plt.xlabel('frame number')
plt.ylabel('JME Error')
plt.legend()

plt.grid(False)
plt.show()
