# -*- coding: utf-8 -*-
# File: views.py
# Author: Alley
# Date  : 2021/1/22
from flask import Blueprint, render_template, request, make_response, jsonify, send_file
import time
import os

dict_month = {
	"1": "Jan.",
	"2": "Feb.",
	"3": "Mar.",
	"4": "Apr.",
	"5": "May",
	"6": "Jun",
	"7": "Jul.",
	"8": "Aug.",
	"9": "Sep.",
	"10": "Oct.",
	"11": "Nov.",
	"12": "Dec."
}

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
	if start_month == end_month and start_year != end_year:
		leftString = "Mean SST(degC) in " + dict_month[str(start_month)] + " " + str(start_year) + "-" + str(end_year)
	elif start_year == end_year and start_month != end_month:
		leftString = "Mean SST(degC) from " + dict_month[str(start_month)] + " to " + dict_month[str(end_month)] + " " + str(start_year)
	elif start_year == end_year and start_month == end_month:
		leftString = "Mean SST(degC) in " + dict_month[str(start_month)] + " " + str(start_year)
	else:
		leftString = "Mean SST(degC) from " + dict_month[str(start_month)] + " to " + dict_month[str(end_month)] + " " + str(start_year) + "-" + str(end_year)
	data = request.args.get("data")
	var = request.args.get('var')
	print(request.args)
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
		fout.write(leftString)
	os.system("ncl /home/alley/work/tyanalyse/project/ncl/sst.ncl")

	return send_file("/home/alley/work/tyanalyse/project/local_pic/result.png")

