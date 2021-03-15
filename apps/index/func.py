from skimage import io
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import  MultipleLocator
from matplotlib.ticker import  FormatStrFormatter
import re
from datetime import datetime
from mongoengine import *
import matplotlib as mpl
import cartopy.crs as ccrs
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import cartopy.feature as cfeature


connect(db='cma', alias='cma', host='mongodb://192.168.0.2:27017/')
# 用于记录每个台风的信息
class Record(EmbeddedDocument):
    line_id = IntField(required=True)
    date = DateTimeField(required=True)
    grade = StringField(required=True)
    loc = PointField(required=True)
    slp = FloatField(required=True)
    v = FloatField(required=True)

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

dict_month = {
	"1": "Jan.",
	"2": "Feb.",
	"3": "Mar.",
	"4": "Apr.",
	"5": "May",
	"6": "Jun.",
	"7": "Jul.",
	"8": "Aug.",
	"9": "Sep.",
	"10": "Oct.",
	"11": "Nov.",
	"12": "Dec."
}


def get_pic_title(var, start_year, end_year, start_month, end_month, level):
    if var == "sst":
        var_part = "SST(degC) in "
    elif var == "height":
        var_part = "Height(dagpm) in "
    elif var == "height_anomaly":
        var_part = "Height Anomaly(dagpm) in "
    elif var == "slp_anomaly":
        var_part = "Sea Level Pressure Anomaly(hPa) in "
    elif var == "sst_anomaly":
        var_part = "SST Anomaly(degC) in "
    elif var == "wind":
        if level == "850":
            var_part = "850hPa Wind(m/s) in "
        elif level == "200":
            var_part = "200hPa Wind(m/s) in "
    elif var == "wind_anomaly":
        if level == "850":
            var_part = "850hPa Wind Anomaly(m/s) in "
        elif level == "200":
            var_part = "200hPa Wind Anomaly(m/s) in "
    else:
        var_part = "None"

    if start_month == end_month and start_year != end_year:
        leftString = var_part + dict_month[str(start_month)] + " " + str(start_year) + "-" + str(end_year)
    elif start_year == end_year and start_month != end_month:
        leftString = var_part + dict_month[str(start_month)] + " to " + dict_month[
            str(end_month)] + " " + str(start_year)
    elif start_year == end_year and start_month == end_month:
        leftString = var_part + dict_month[str(start_month)] + " " + str(start_year)
    else:
        leftString = var_part + dict_month[str(start_month)] + " to " + dict_month[
            str(end_month)] + " " + str(start_year) + "-" + str(end_year)
    return leftString

def corp_margin(img):
    img2=img.sum(axis=2)
    (row,col)=img2.shape
    row_top=0
    row_down=0
    col_top=0
    col_down=0
    for r in range(0,row):
        if img2.sum(axis=1)[r]<765*col:
            row_top=r
            break

    for r in range(row-1,0,-1):
        if img2.sum(axis=1)[r]<765*col:
            raw_down=r
            break

    for c in range(0,col):
        if img2.sum(axis=0)[c]<765*row:
            col_top=c
            break

    for c in range(col-1,0,-1):
        if img2.sum(axis=0)[c]<765*row:
            col_down=c
            break

    new_img=img[row_top-10:raw_down+10,col_top-10:col_down+10,0:3]
    return new_img

# 旧的读文件的画法
# def draw_frequency(start_year, start_month, end_year, end_month):
    # 这两个参数的默认可使列名对齐
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)

    ##########################################################################
    # 1. 读数据
    ##########################################################################
    start_year = int(start_year)
    end_year = int(end_year)
    start_month = int(start_month)
    end_month = int(end_month)
    month_list = range(start_month, end_month + 1)

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
    y11 = [sum(y) / len(y)] * len(y)
    print(y)
    print(y11)

    # 根据y的最小值和最大值，计算纵坐标的范围 #####################################
    def calculate_y_range(y):
        y_min = min(y)
        y_max = max(y)
        for i in range(0, 41, 5):
            if y_min <= i:
                bottom = i - 5
                break
        for i in range(40, -1, -5):
            if y_max >= i:
                top = i + 5
                break
        return [bottom, top]

    bottom, top = (calculate_y_range(y))
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
    plt.figure(figsize=(10, 6))
    # 1.1 画年变化在上
    ax1 = plt.subplot(111)
    ax1.set_xlim(start_year - 1, end_year + 2)
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

    ax1.set_title(title, fontdict={'weight': 'normal', 'size': 20})  # 不能出现中文
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Frequency')
    # ax1.figure(num=1,figsize=(15,5))
    ax1.plot(x, y, color="r", linewidth=2.0)
    ax1.plot(x, y11, color="blue", linewidth=2.0, linestyle="--", label="mean")
    ax1.scatter(x, y, s=50, c="r", alpha=1, )
    ax1.text(x[-2], y11[0]-0.5, format(y11[0],'.1f'), c="blue")
    ax1.legend()
    plt.grid(axis='y')  # 添加网格
    plt.savefig("/home/alley/work/tyanalyse/project/local_pic/result.png", dpi=300, bbox_inches='tight')




