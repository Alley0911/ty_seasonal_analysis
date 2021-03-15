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


def draw_tracks(start_year, start_month, end_year, end_month, title):
    def map_grade_to_color(grades):
        colors = []
        for grade in grades:
            if grade == 'TS':
                colors.append('b')
            elif grade == "STS":
                colors.append('y')
            elif grade == "TY":
                colors.append('orange')
            elif grade == "STY":
                colors.append('pink')
            elif grade == "SuperTY":
                colors.append('r')
        return colors
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
    months = range(start_month, end_month + 1)
    years = range(start_year, end_year + 1, 1)
    x = years
    ty_records = []

    # 指定年份的台风的记录
    data_tmp = Typhoons.objects(generation_year__in=years, generation_month__in=months)
    for i in (data_tmp):
        name = i.name
        lons = []
        lats = []
        grades = []
        records = i.records
        for record in records:
            lons.append(record.loc['coordinates'][0])
            lats.append(record.loc['coordinates'][1])
            grades.append((record.grade))
        dict_tmp = {"name":name, "lons":lons, "lats":lats, "grades":grades}
        ty_records.append(dict_tmp)
    # print(len(ty_records))
    #########################################################################
    # 1. 画图
    #########################################################################
    # 经纬度范围
    lat_min = 0
    lat_max = 50
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
    for ty_record in ty_records:
        name = ty_record["name"]
        lons = ty_record['lons']
        lats = ty_record['lats']
        grades = ty_record['grades']
        colors = map_grade_to_color(grades)
        ax.scatter(lons, lats, s=30, c=colors)
        ts = ax.scatter([50], [-50], s=25, c='b')
        sts = ax.scatter([50], [-50], s=25, c='y')
        ty = ax.scatter([50], [-50], s=25, c='orange')
        sty = ax.scatter([50], [-50], s=25, c='pink')
        superty = ax.scatter([50], [-50], s=25, c='r')
        ax.plot(lons, lats, c='k')
        ax.annotate(name, (lons[0], lats[0]), xycoords='data',xytext=(lons[0]+0.5, lats[0]+0.5))
    plt.legend((ts, sts, ty, sty, superty), ('TS', 'STS','TY', 'STY', 'SuperTY'))
    plt.savefig("/home/alley/work/tyanalyse/project/local_pic/result.png", dpi=300, bbox_inches='tight')
if __name__ == "__main__":
    draw_tracks(2019, 1, 2019, 12)