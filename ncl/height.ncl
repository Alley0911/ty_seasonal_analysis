load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"  
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"  
;************************************************
begin

; 获取各种参量
args = asciiread("/home/alley/work/tyanalyse/project/ncl/params.txt", -1, "string")
start_year = stringtoint(args(0))
start_month = stringtoint(args(1))
end_year = stringtoint(args(2))
end_month = stringtoint(args(3))
north = stringtoint(args(4))
south = stringtoint(args(5))
west = stringtoint(args(6))
east = stringtoint(args(7))
data = (args(8))
var = (args(9))
leftstring = (args(10))
level = stringtoint(args(11))
filepath = "/home/alley/data/" + data + "/Height/"
pic_name = "/home/alley/work/tyanalyse/project/local_pic/result"

; 获取需要的文件名
number = (end_year - start_year + 1) * (end_month - start_month +1)
files_cur = new(number, string)
n = 0
do y = start_year, end_year
    do m = start_month, end_month
        if (m .le. 9) then
            files_cur(n) = filepath + "height_" + y + "0" + m + ".grb"
        else
            files_cur(n) = filepath + "height_" + y + m + ".grb"
        end if
        n = n + 1
    end do
end do


; 获取目标场的平均
f    = addfiles (files_cur, "r")
ListSetType(f, "join")
height = f[:]->Z_GDS0_ISBL_S123
; printVarSummary(height)
height = height/98

if dimsizes(files_cur) .eq. 1 then
    ; print(dimsizes(files))
    height_avg = height
else
    height_avg = dim_avg_n_Wrap(height, 0)
end if
height_avg@long_name = ""
height_avg@units = ""

wks = gsn_open_wks("png", pic_name)                  ; send graphics to PNG file
res = True
res@gsnDraw = False
res@gsnFrame = False
res@mpShapeMode = "FreeAspect"
res@vpWidthF = 0.8
res@vpHeightF = 0.6
res@vpXF = 0.1
res@vpYF = 0.8
res@mpMaxLatF = north
res@mpMinLatF = south
res@mpMinLonF = west
res@mpMaxLonF = east
res@tmXTOn = False
res@tmYROn = False
res@mpCenterLonF = 150
; res@tiMainFontHeightF = 0.022
res@tiMainOffsetYF = -0.02
res@cnLevelSelectionMode="ExplicitLevels"
res@cnLevels = ispan(500, 640, 4)
; res@cnMonoLineThickness = False
; res@cnLineThicknesses = 
res@tiMainString = leftstring
res@tiMainOffsetYF = -0.015
res@cnLineThicknessF=5
res@cnInfoLabelOn=False
res@cnLineColor="blue"
res@cnLineLabelInterval=1
res@cnLineLabelFontHeightF=0.010
plot = gsn_csm_contour_map_ce(wks, height_avg, res)         ; create a default plot
dir      = "/home/alley/data/ncl/GSHHS_shp/"
filename = "l/GSHHS_l_L1.shp"
dum  = gsn_add_shapefile_polylines(wks,plot,dir+filename,True)
draw(plot)
frame(wks)
end
