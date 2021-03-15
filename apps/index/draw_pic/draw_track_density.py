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


def draw_track_density(start_year, start_month, end_year, end_month, title):
    # 这两个参数的默认可使列名对齐
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)

    # 台风路径密度格点
    lon_grid = np.arange(100, 180.1, 2.5)
    lat_grid = np.arange(0, 90.1, 2.5)
    density = np.zeros((len(lat_grid), len(lon_grid)), dtype=int)
    # print(lon_grid.shape)
    # print(lat_grid.shape)
    # print(density.shape)
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


    # 指定年份的台风的记录
    data_tmp = Typhoons.objects(generation_year__in=years, generation_month__in=months)
    for i in (data_tmp):
        lon = []
        lat = []
        # print(i.name)
        records = i.records
        for record in records:
            lon.append(record.loc['coordinates'][0])
            lat.append(record.loc['coordinates'][1])


        # 用于存放离台风经纬度最近的格点
        lon_adjust = []
        lat_adjust = []
        for lon_tmp, lat_tmp in zip(lon, lat):
            for lon_g, lat_g in zip(lon_grid, lat_grid):
                if abs(lon_tmp - lon_g)<=1.25:
                    lon_adjust.append(lon_g)
                if abs(lat_tmp - lat_g)<=1.25:
                    lat_adjust.append(lat_g)
        # print(len(lon_adjust))
        # print(len(lat_adjust))

        # 考虑6小时间隔的台风路径密度，同时为了和ACE保持一致，将去重这一项去掉
    # 去重,假如台风在某地停留则该地只加1，不会重复加1;
        # loc = []
        # for lon_a, lat_a in zip(lon_adjust, lat_adjust):
        #     loc.append([lon_a, lat_a])
        # loc_no_dup = []
        # for i in loc:
        #     if i not in loc_no_dup:
        #         loc_no_dup.append(i)
        # lon_adjust = [x[0] for x in loc_no_dup]
        # lat_adjust = [x[1] for x in loc_no_dup]
        # # print(len(lon_adjust))
        # print(len(lat_adjust))

    # 计算路径密度

    # print(density.shape)
        for index_lat, lat_ in enumerate(lat_grid):
            for index_lon, lon_ in enumerate(lon_grid):
                for lon_ty,lat_ty in zip(lon_adjust, lat_adjust):
                    if lon_ty == lon_ and lat_ty == lat_:
                        density[index_lat, index_lon] += 1
    max_value = (np.nanmax(density))
    #########################################################################
    # 1. 画图
    #########################################################################
    # 经纬度范围
    lat_min = 0
    lat_max = 50
    lon_min = 100
    lon_max = 180

    # norm = plt.Normalize(vmin=np.min(density),vmax=np.max(density))


    #
    fig = plt.figure(figsize=(12, 8), dpi=200)
    ax = fig.add_subplot(projection=ccrs.PlateCarree())
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
    # cn = ax.contourf(lon_grid, lat_grid, density,cmap='Greens',levels=range(1, max_value+1, 1), transform=ccrs.PlateCarree(),extend='both')
    # rotated_pole = ccrs.RotatedPole(pole_longitude=177.5, pole_latitude=37.5)
    cn = ax.pcolor(lon_grid, lat_grid, density, shading='flat', cmap="Reds")
    # plt.pcolormesh(density, shading='flat')
    plt.colorbar(cn, fraction=0.030)
    plt.savefig("/home/alley/work/tyanalyse/project/local_pic/result.png", dpi=300, bbox_inches='tight')
if __name__ == "__main__":
    draw_tracks(2019, 1, 2019, 12)