# 1、平均生成经度、纬度
# 2、平均生命周期
# 3、平均风速
# 4、平均海平面气压

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


# 根据lat的最小值和最大值，计算纵坐标的范围 #####################################



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


def draw_generation_location(start_year, start_month, end_year, end_month, title):
    def calculate_range(list_value):
        list_value_min = np.array(list_value).min()
        list_value_max = np.array(list_value).max()
        for i in range(0, 90, 2):
            if list_value_min <= i:
                bottom = i - 2
                break
        for i in range(90, 0, -2):
            if list_value_max >= i:
                top = i + 2
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
    lat = []
    lon = []

    # 指定年份的经纬度变化
    data_tmp = Typhoons.objects(generation_year__in=years, generation_month__in=months)

    for i in (data_tmp):
        lat_tmp = (i.generation_loc['coordinates'][1])
        lon_tmp = (i.generation_loc['coordinates'][0])
        lat.append(lat_tmp)
        lon.append(lon_tmp)

    #########################################################################
    # 1. 画图
    #########################################################################
    # 经纬度范围
    lat_min = 0
    lat_max = 40
    lon_min = 100
    lon_max = 180


    fig = plt.figure(figsize=(12, 8), dpi=200)
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    dlon, dlat = 10, 10
    xticks = np.arange(lon_min, lon_max + 0.1, dlon)
    yticks = np.arange(lat_min, lat_max + 0.1, dlat)
    ax.add_feature(cfeature.COASTLINE, lw=0.25)
    ax.add_feature(cfeature.LAND)
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=False, lw=1, linestyle=':', color='k', alpha=0.8)
    gl.xlocator = mticker.FixedLocator(xticks)
    gl.ylocator = mticker.FixedLocator(yticks)
    ax.set_xticks(xticks, crs=ccrs.PlateCarree())
    ax.set_yticks(yticks, crs=ccrs.PlateCarree())
    ax.xaxis.set_major_formatter(LongitudeFormatter())
    ax.yaxis.set_major_formatter(LatitudeFormatter())
    extent = [lon_min, lon_max, lat_min, lat_max]  # 设置图显示的经纬度范围
    ax.set_extent(extent, crs=ccrs.PlateCarree())
    ax.set_title(title, size=15)
    ax.xaxis.set_tick_params(labelsize=10)
    ax.yaxis.set_tick_params(labelsize=10)
    ax.scatter(lon, lat, s=30, c='r')
    plt.savefig("/home/alley/work/tyanalyse/project/local_pic/result.png", dpi=300, bbox_inches='tight')

if __name__ == "__main__":
    draw_generatation_location(2019, 11, 2019, 11)
