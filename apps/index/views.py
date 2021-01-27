# -*- coding: utf-8 -*-
# File: views.py
# Author: Alley
# Date  : 2021/1/22
from flask import Blueprint, render_template, request, make_response, jsonify, send_file
import time
import os
from apps.index.func import *

index_bp = Blueprint('index', __name__)


@index_bp.route('/')
def index():
	return render_template("index.html")

@index_bp.route('/draw_pic', methods=['get'], )
def draw_pic():
	method = request.method
	res = make_response(jsonify(token=123456, gender=0, method = method))  # 设置响应体
	res.status = '200'# 设置状态码
	res.headers['Access-Control-Allow-Origin'] = "*"# 设置允许跨域
	res.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'

	start_year = request.args.get("start_year")
	start_month = request.args.get("start_month")
	end_year = request.args.get("end_year")
	end_month = request.args.get("end_month")
	north = request.args.get("north")
	south = request.args.get("south")
	west = request.args.get("west")
	east = request.args.get('east')
	data = request.args.get("data")
	var = request.args.get('var')
	level = request.args.get("level")
	leftString = get_pic_title(var, start_year, end_year, start_month, end_month, level)
	with open("/home/alley/work/tyanalyse/project/ncl/params.txt", 'w') as fout:
		fout.write(start_year + "\n")
		fout.write(start_month + "\n")
		fout.write(end_year + "\n")
		fout.write(end_month + "\n")
		fout.write(north + "\n")
		fout.write(south + "\n")
		fout.write(west + "\n")
		fout.write(east + "\n")
		fout.write(data + "\n")
		fout.write(var + "\n")
		fout.write(leftString + "\n")
		fout.write(level)


	if var == "sst":
		os.system("ncl /home/alley/work/tyanalyse/project/ncl/sst.ncl")
	elif var == "height":
		os.system("ncl /home/alley/work/tyanalyse/project/ncl/height.ncl")
	elif var == "sst_anomaly":
		os.system("ncl /home/alley/work/tyanalyse/project/ncl/sst_anomaly.ncl")
	elif var == "wind":
		os.system("ncl /home/alley/work/tyanalyse/project/ncl/wind.ncl")
	elif var == 'frequency':
		draw_frequency(start_year, start_month, end_year, end_month)

	if var != "frequency":
		im = io.imread("/home/alley/work/tyanalyse/project/local_pic/result.png")
		img_re = corp_margin(im)
		io.imsave('/home/alley/work/tyanalyse/project/local_pic/result.png', img_re)

	return send_file("/home/alley/work/tyanalyse/project/local_pic/result.png")

