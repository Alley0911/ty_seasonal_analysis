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


# 根据lon的最小值和最大值，计算纵坐标的范围 #####################################



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



def draw_generation_lon(start_year, start_month, end_year, end_month, title):
    def calculate_range(list_value):
        list_value_min = np.nanmin(np.array(list_value))
        list_value_max = np.nanmax(np.array(list_value))
        for i in range(0, 180, 5):
            if list_value_min <= i:
                bottom = i - 5
                break
        for i in range(180, 0, -5):
            if list_value_max >= i:
                top = i + 5
                break
        return [bottom, top]

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
    lon = []

    # 指定年份的经纬度变化
    for year in years:
        data_tmp = Typhoons.objects(generation_year=year, generation_month__in=months)
        lon_mean = []

        for i in (data_tmp):
            lon_tmp = (i.generation_loc['coordinates'][0])
            lon_mean.append(lon_tmp)
        lon.append(np.nanmean(lon_mean))
    print(lon)
    #  求指定年份的平均
    lon_mean_of_selected = [np.nanmean(lon)]*len(lon)


    # 求气候场平均
    lon_cli = []
    for year in range(1981, 2011):
        data_tmp = Typhoons.objects(generation_year=year, generation_month__in=months)
        lon_mean = []

        for i in (data_tmp):
            lon_tmp = (i.generation_loc['coordinates'][0])
            lon_mean.append(lon_tmp)
        lon_cli.append(np.nanmean(lon_mean))
    lon_cli = [np.nanmean(lon_cli)] * len(lon)


    lon_bottom, lon_top = (calculate_range(lon))
    #########################################################################
    # 1. 画图
    #########################################################################
    plt.figure(figsize=(10, 6))
    # 1.1 画年变化在上
    ax1 = plt.subplot(111)
    ax1.set_xlim(start_year - 1, end_year + 2)
    ax1.set_ylim((lon_bottom, lon_top))
    print(lon_bottom)
    print(lon_top)
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

    ax1.set_title(title, fontdict={'weight': 'normal', 'size': 20})  # 不能出现中文
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Longitude')
    # ax1.figure(num=1,figsize=(15,5))
    ax1.plot(x, lon, color="r", linewidth=2.0)
    ax1.plot(x, lon_mean_of_selected, color="blue", linewidth=2.0, linestyle="--", label="mean")
    ax1.plot(x, lon_cli, color="g", linewidth=2.0, linestyle="--", label="climate_mean")
    ax1.scatter(x, lon, s=50, c="r", alpha=1,)
    ax1.legend()
    plt.grid(axis='y')  # 添加网格
    plt.savefig("/home/alley/work/tyanalyse/project/local_pic/result.png", dpi=300, bbox_inches='tight')

if __name__ == "__main__":
    draw_generation_lon(1981, 11, 2019, 11)
