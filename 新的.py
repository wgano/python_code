import paddle  # --->PaddlePaddle深度学习框架
import numpy as np # --->python基本库，用于科学计算
import os #--->python的模块，可使用该模块对操作系统进行操作
import matplotlib.pyplot as plt  #--->python绘图库，可方便绘制折线图、散点图等图形
paddle.set_default_dtype("float64")
data_line = 'F:\data.txt'
data = np.fromfile(data_line, sep=' ')
print(data.shape)