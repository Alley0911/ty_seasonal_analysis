# 1、平均生成经度、纬度
# 2、平均生命周期
# 3、平均风速
# 4、平均海平面气压

from skimage import io
import os
import pandas as pd
import numpy as np
from numpy import *  # import这个后可以直接使用mean()函数
import matplotlib.pyplot as plt
from matplotlib.ticker import  MultipleLocator
from matplotlib.ticker import  FormatStrFormatter
import linecache
import re
from datetime import datetime
from mongoengine import *

connect(db='cma', alias='cma', host='mongodb://192.168.0.2:27017/')
# 用于记录每个台风的信息
class Record(EmbeddedDocument):
    line_id = IntField(required=True)
    date = DateTimeField(required=True)
    grade = StringField(required=True)
    loc = PointField(required=True)
    slp = FloatField(required=True)
    v = FloatField(required=True)

# 类声明
# 当创建实例后会自动添加一个typhoons的集合
class Typhoons(DynamicDocument):
    name = StringField(required=True)
    ty_id = IntField(required=True, unique=True)
    is_land = BooleanField(required=True)  # 是否登陆
    records = ListField(EmbeddedDocumentField(Record))
    generation_year = IntField(required=True)  # 生成的年份
    generation_month = IntField(required=True)  # 生成的月份
    generation_loc = PointField(required=True)  # 生成经纬度
    duration = FloatField(required=True)  # 持续时间及生命周期，单位为天
    meta={
        'db_alias': 'cma'
    }


def draw_ace(start_year, start_month, end_year, end_month, title):
    # def calculate_range(list_value):
    #     list_value_min = np.nanmin(np.array(list_value))
    #     list_value_max = np.nanmax(np.array(list_value))
    #     top = int(list_value_max)/10 + 1
    #     dd = top
    #     print(list_value_min)
    #     print(list_value_max)
    #     for i in range(0, 100, 2):
    #         if list_value_min <= i:
    #             bottom = i - 2
    #             break
    #     for i in range(100, 0, -2):
    #         if list_value_max >= i:
    #             top = i + 2
    #             break
    #     return [bottom, top]

    ##########################################################################
    # 1. 读数据
    ##########################################################################
    start_year = int(start_year)
    end_year = int(end_year)
    start_month = int(start_month)
    end_month = int(end_month)
    months = range(start_month, end_month + 1)
    years = range(start_year, end_year + 1, 1)
    x = years
    ace = []

    # 指定年份的经纬度变化
    for year in years:
        # print(year)
        data_tmp = Typhoons.objects(generation_year=year, generation_month__in=months)
        ace_sum= []
        for i in (data_tmp):
            # print(i.ty_id)
            ace_tmp = []
            records = i.records
            for record in records:
                ace_tmp.append(record.v**2 * 10**-4)
            ace_sum.append(np.nansum(ace_tmp))
        ace.append(np.nansum(ace_sum))

    #  求指定年份的平均
    ace_mean_of_selected = [np.nanmean(ace)]*len(ace)
 
    # 求气候场平均
    ace_cli= []
    # 气候场
    for year in range(1981, 2011):
        data_tmp = Typhoons.objects(generation_year=year, generation_month__in=months)
        ace_sum= []
        for i in (data_tmp):
            # print(i.ty_id)
            ace_tmp = []
            records = i.records
            for record in records:
                ace_tmp.append(record.v**2 * 10**-4)
            ace_sum.append(np.nansum(ace_tmp))
        ace_cli.append(np.nansum(ace_sum))
    ace_cli = [np.nanmean(ace_cli)] * len(ace)
    # ace_bottom, ace_top = (calculate_range(ace))

    #########################################################################
    # 1. 画图
    #########################################################################
    plt.figure(figsize=(10, 6))
    # 1.1 画年变化在上
    ax1 = plt.subplot(111)
    ax1.set_xlim(start_year-1, end_year + 2)
    # ax1.set_ylim((ace_bottom, ace_top))
    # ax1.set_yticks=list(range(ace_bottom, ace_top+1,5))
    # ax1.set_yticklabels=list(range(ace_bottom, ace_top+1,5))
    # 主副刻度设置
    # 将x主刻度标签设置为5的倍数(也即以 5为主刻度单位其余可类推)
    xmajorLocator = MultipleLocator(2)
    # 设置x轴标签文本的格式
    xmajorFormatter = FormatStrFormatter('%d')
    # 将x轴次刻度标签设置为1的倍数
    xminorLocator = MultipleLocator(1)
    # 设置主刻度标签的位置,标签文本的格式
    ax1.xaxis.set_major_locator(xmajorLocator)
    ax1.xaxis.set_major_formatter(xmajorFormatter)
    # 显示次刻度标签的位置,没有标签文本
    ax1.xaxis.set_minor_locator(xminorLocator)

    # # 主副刻度设置
    # # 将y主刻度标签设置为5的倍数(也即以 5为主刻度单位其余可类推)
    # ymajorLocator = MultipleLocator(2)
    # # 设置x轴标签文本的格式
    # ymajorFormatter = FormatStrFormatter('%d')
    # # 将x轴次刻度标签设置为1的倍数
    # yminorLocator = MultipleLocator(1)
    # # 设置主刻度标签的位置,标签文本的格式
    # ax1.yaxis.set_major_locator(ymajorLocator)
    # ax1.yaxis.set_major_formatter(ymajorFormatter)
    # # 显示次刻度标签的位置,没有标签文本
    # ax1.yaxis.set_minor_locator(yminorLocator)

    ax1.set_title(title, fontdict={'weight': 'normal', 'size': 20})  # 不能出现中文
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Latitude')
    # ax1.figure(num=1,figsize=(15,5))
    ax1.plot(x, ace, color="r", linewidth=2.0)
    ax1.plot(x, ace_mean_of_selected, color="blue", linewidth=2.0, linestyle="--", label="mean")
    ax1.plot(x, ace_cli, color="g", linewidth=2.0, linestyle="--", label="climate_mean")
    ax1.scatter(x, ace, s=50, c="r", alpha=1,)
    ax1.legend()
    plt.grid(axis='y')  # 添加网格
    plt.savefig("/home/alley/work/tyanalyse/project/local_pic/result.png", dpi=300, bbox_inches='tight')

if __name__ == "__main__":
    draw_ace(1981, 11, 2019, 11)
