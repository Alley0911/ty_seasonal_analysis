import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import  MultipleLocator
from matplotlib.ticker import  FormatStrFormatter

# 这两个参数的默认可使列名对齐
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)

##########################################################################
# 1. 读数据
##########################################################################
start_year = 1981
end_year = 2019
start_month = 11
end_month = 12
month_list = range(start_month, end_month+1)

begin1 = start_year
end1 = end_year
# if begin1 == end1:
sel_year = begin1
num1 = end1 - begin1 + 1
res_in = pd.read_excel("/home/alley/data/TY_best_track/台风月频数变化.xls", index_col=0)  # 将表格文件第一列作为res_in的index
# print(res_in)
# print(res_in.index)
years = range(begin1, end1 + 1, 1)
x = years
# y1 = res_in.loc["总计", years]
y1 = res_in.loc[month_list, years]
y = y1.sum(axis=0)  # 计算所求的几个月的频数和
y11 = [sum(y)/len(y)] * len(y)
print(y11)
# 根据y的最小值和最大值，计算纵坐标的范围 #####################################
def calculate_y_range(y):
	y_min = min(y)
	y_max = max(y)
	for i in range(0,41,5):
		if y_min >=i:
			bottom = i
			break
	for i in range(40,-1,-5):
		if y_max >= i:
			top = i
			break
	return [bottom, top]
bottom, top = (calculate_y_range(y))
print(y)
print(min(y))
print(bottom)
title_prefix = "Frequency Time Series of Typhoons "
def get_title(start_month, end_month):
    if start_month == end_month:
        leftString = title_prefix + "in " + dict_month[str(start_month)]
    elif start_month != end_month:
        leftString = title_prefix + "from " + dict_month[str(start_month)] + " to " + dict_month[str(end_month)]
    return leftString
title = get_title(start_month, end_month)
#########################################################################
# 1. 画图
#########################################################################
plt.figure(figsize=(10,6))
# 1.1 画年变化在上
ax1 = plt.subplot(111)
ax1.set_xlim(start_year-1, end_year+2)
ax1.set_ylim((bottom, top))

# 主副刻度设置
# 将x主刻度标签设置为5的倍数(也即以 5为主刻度单位其余可类推)
xmajorLocator = MultipleLocator(5)
# 设置x轴标签文本的格式
xmajorFormatter = FormatStrFormatter('%d') 
# 将x轴次刻度标签设置为1的倍数
xminorLocator = MultipleLocator(1)
# 设置主刻度标签的位置,标签文本的格式
ax1.xaxis.set_major_locator(xmajorLocator)
ax1.xaxis.set_major_formatter(xmajorFormatter)
# 显示次刻度标签的位置,没有标签文本
ax1.xaxis.set_minor_locator(xminorLocator)


ax1.set_title(title,fontdict={'weight':'normal','size': 20})  # 不能出现中文
ax1.set_xlabel('Year')
ax1.set_ylabel('Frequency')
# ax1.figure(num=1,figsize=(15,5))
ax1.plot(x, y, color="r", linewidth=2.0)
ax1.plot(x, y11, color="blue", linewidth=2.0, linestyle="--", label="mean")
ax1.scatter(x, y, s=50, c="r", alpha=1,)
# ax1.text(2018, y1_avg-3, y1_avg, c="blue")
ax1.legend()

#########################################################################

# ax2 = plt.subplot(212)
# ax2.set_xlim((0, 13))
# ax2.set_ylim((0, 10))
# ax2.set_xlabel('Month')
# ax2.set_ylabel('Frequency')
# ax2.set_xticks(range(1, 13))
# ax2.set_yticks(range(0, 11))
# x2 = months
# y21 = df_month["均值"]
# y22 = df_month["最大值"]
# y23 = df_month["最小值"]
# y24 = df_month[sel_year]
# print(y24)
# ax2.plot(x2, y21, color="k", label="mean")
# ax2.scatter(x2, y21, color="k")
# ax2.plot(x2, y22, color="b", label="max")
# ax2.scatter(x2, y22, color="b")
# ax2.plot(x2, y23, color="g", label="min")
# ax2.scatter(x2, y23, color="g")
# ax2.plot(x2, y24, color="r", label=str(sel_year))
# ax2.scatter(x2, y24, color="r")
# # df_month.plot(x="index", y=["min"], ax=ax2, color="b")
# # df_month.plot.scatter(x="index", y=["min"], color="b", ax=ax2)
# # df_month.plot(x="index", y=["max"], ax=ax2, color="g")
# # df_month.plot.scatter(x="index", y=["max"], color="g", ax=ax2)
# # df_month.plot.scatter(x="index", y=["min"], ax=ax2)
# # df_month.plot.scatter(x="index", y=["max"], ax=ax2)
# ax2.legend()  # 加上这一句 label 才能显示
plt.grid(axis='y')  # 添加网格
# plt.show()
plt.savefig("/home/alley/work/tyanalyse/project/local_pic/result.png",dpi=300, bbox_inches = 'tight')
