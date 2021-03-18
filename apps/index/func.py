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
        elif level == "500":
            var_part = "500hPa Wind(m/s) in "
        elif level == "200":
            var_part = "200hPa Wind(m/s) in "
    elif var == "wind_anomaly":
        if level == "850":
            var_part = "850hPa Wind Anomaly(m/s) in "
        elif level == "200":
            var_part = "200hPa Wind Anomaly(m/s) in "
        elif level == "500":
            var_part = "500hPa Wind Anomaly(m/s) in "
    elif var == 'track_density':
        var_part = "Track Density of TCs in "
    elif var == 'ace_distribution':
        var_part = "ACE(10\u2074 m/s\u00b2) of TCs in "
    elif var == 'generatation_location':
        var_part = "Gneration Location of TCs in "
    elif var == 'generation_lat':
        var_part = "Genration Latitude of TCs in "
    elif var == 'generation_lon':
        var_part = "Genration Longitude of TCs in "
    elif var == 'mean_lat':
        var_part = "Mean Latitude of TCs in "
    elif var == 'mean_lon':
        var_part = "Mean Longitude of TCs in "
    elif var == 'ace':
        var_part = "ACE(10\u2074 m/s\u00b2) of TCs in "
    elif var == 'tracks':
        var_part = "Tracks of TCs in "
    elif var == 'frequency':
        var_part = "Frequency of TCs in "
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




