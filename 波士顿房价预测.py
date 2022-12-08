# 任务可能用到的宏包
import paddle  # --->PaddlePaddle深度学习框架
import numpy as np # --->python基本库，用于科学计算
import os #--->python的模块，可使用该模块对操作系统进行操作
import matplotlib.pyplot as plt  #--->python绘图库，可方便绘制折线图、散点图等图形
import paddle.nn.functional as F

## 步骤一：读入数据，分析数据
#设置默认的全局dtype为float64
paddle.set_default_dtype("float64")
#加载数据集---->需要使用到的函数 np.fromfile()
#-------------<    请键入你的代码    >------------#
data_file = 'F:\edgedownload\housing.data'#文件地址
data = np.fromfile(data_file, sep=' ')#文件数据保存在data并以空格为分隔符分割元素保存为列表元素

## 数据组织
# 打印观察数据的维数---->可能使用的函数 shape
#-------------<    请键入你的代码    >------------#
print(data.shape)#打印data的保存形式这里是一维数组

## 得到的数据Data是一个一维数组，我们接下来需要把这个一维数组变为我们所需要的形式---> 一行数据，从左往右依次是13个因变量x，1个自变量 y
# 根据数据集确定需要使用的变量（自变量+因变量）
#-------------<    请键入你的代码    >------------#
feature_names = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTATA','MEDV']#相当于键,对应表头
feature_num = len(feature_names)  # 特征值数量,取表头数,按此数将data切片

# 重塑数据大小，需要使用的函数 reshape(), 以及 整除运算符号 //
#-------------<    请键入你的代码    >------------#
data = data.reshape([data.shape[0] // feature_num, feature_num])#data.shape[0]代表行数,1代表列数,这里是一维数组应该就是代表元素个数,这里reshape表示改为二维数组且两个变量规定了行数和列数

# 再次打印观察数据的维数
#-------------<    请键入你的代码    >------------#
print(feature_num)
print(data.shape)
# 至此，我们已经将数据转换为一个矩阵的形式（二维数组），矩阵的每一行有14个元素，代表一组数据

# 接下来，我们来使用 matplotlib 将数据画出来，观察一下, 需要用到的函数为 plt.plot
# 分别画出14个变量的变化趋势，并标注坐标轴的含义 （横轴可以用 K 来表示第几组数据）
# 或者画出自变量-因变量的散点图
#-------------<    请键入你的代码    >------------#



# for feature_index in range(0, 13):  #  利用 for 循环 画出自变量-因变量的散点图（折线图），feature_index 为变量的下标，取值为 0，……，13
#     x_datas = data[:,feature_index]  # 数据切片，利用 feature_index 索引第 feature_index 个 变量,x轴数据依次取第n个一维数组
#     y_datas = data[:,-1]             # data 数组的最后一列为 因变量————房屋的价格
#     fig = plt.figure()     # 开始绘图
#     ax = fig.add_axes([0,0,1,1])#这四个参数分别表示以移动,上移动,横向压缩,竖直压缩百分比建图
#     ax.scatter(x_datas, y_datas, label=feature_names[feature_index])#布置散点
#     ax.set_xlabel(feature_names[feature_index])#x轴标签
#     ax.set_ylabel(feature_names[-1])#y轴标签
#     ax.set_title(f"{feature_names[-1]} - {feature_names[feature_index]}")#顶部标题
#     plt.legend()#使用plt.legend( )使上述代码产生效果
# plt.show()


# 训练集-测试集划分：一般训练集和测试集的样本数比值为 8:2
# 因此，我们可以取 506 条数据的 80% 为训练样本，剩余的为测试样本

# 1. 计算训练样本的数目
#-------------<    请键入你的代码    >------------#
ratio=0.8
offset=int(data.shape[0]*ratio)


# 2. 对数据进行切片得到训练数据样本集 以及测试样本集
# 打印观察训练样本和测试样本的shape
#-------------<    请键入你的代码    >------------#
training_data=data[:offset]
test_data=data[offset:]


# 数据的归一化处理
# 我们从原始数据/子任务1中的图中可以明显看出，各个变量的取值范围（值域）差别很大
# 例如 LSTAT（低收入人群占比）取值为 0~40 ; 而 TAX（全值财产税率）取值范围约为 100~800 ;
# 直接对原始数据进行回归训练效率较低
# 因此，可以将所有特征值的取值等比例放缩到 相同的取值范围之间 (0~1)（归一化处理），以提升训练效率
# ！！！ 注意：训练集和测试集都需要归一化，而且训练集需要用测试集的 最大值/最小值/平均值 进行缩放

# 1. 计算训练集的最大值、最小值、平均值，并打印输出
#-------------<    请键入你的代码    >------------#
maxmums,minmums,avgs=training_data.max(axis=0),training_data.min(axis=0),training_data.sum(axis=0)/training_data.shape[0]
#axis = 0指的是取二维数组的y轴上的所有数字

# 2. 对训练集以及测试集进行归一化
# 0 ~ 1   （data - min) /（max-min）
#-------------<    请键入你的代码    >------------#
for i in range(feature_num):
    data[:,i]=(data[:,i]-avgs[i])/(maxmums[i]-minmums[i])
train_data=data[:offset]
test_data=data[offset:]




# 接下来，我们来使用 matplotlib 将归一化后的训练集数据画出来，观察一下, 需要用到的函数为 plt.plot
#-------------<    请键入你的代码    >------------#
x = training_data[:, :-1]
y = training_data[:, -1:]
print(x[0], y[0])
for i in range(14):
    m=train_data[:,i]
    plt.plot(range(404),m)
    plt.show()