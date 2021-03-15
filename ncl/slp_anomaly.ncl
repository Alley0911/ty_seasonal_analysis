load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"  
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"  
;************************************************
begin
value = new(62,integer)
value = 5
value(22) = 9
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
filepath = "/home/alley/data/" + data + "/SLP/"
pic_name = "/home/alley/work/tyanalyse/project/local_pic/result"

number = (end_year - start_year + 1) * (end_month - start_month +1)
files_cur = new(number, string)
n = 0
do y = start_year, end_year
    do m = start_month, end_month
        if (m .le. 9) then
            files_cur(n) = filepath + "SLP_" + y + "0" + m + ".grb"
        else
            files_cur(n) = filepath + "SLP_" + y + m + ".grb"
        end if
        n = n + 1
    end do
end do
; print(files_cur)

; 根据时间获取所需要的气候态的文件
number = 30 * (end_month - start_month +1)
files_cli = new(number, string)
n = 0
do y = 1981, 2010
    do m = start_month, end_month
        if (m .le. 9) then
            files_cli(n) = filepath + "SLP_" + y + "0" + m + ".grb"
        else
            files_cli(n) = filepath + "SLP_" + y + m + ".grb"
        end if
        n = n + 1
    end do
end do
; print(files_cli)
; 获取目标场的平均
f_cur    = addfiles (files_cur, "r")
ListSetType(f_cur, "join")
slp_cur = f_cur[:]->MSL_GDS0_SFC_S123
slp_cur = slp_cur / 100
; printVarSummary(slp)

if dimsizes(files_cur) .eq. 1 then
    ; print(dimsizes(files))
    slp_avg_cur = slp_cur
else
    slp_avg_cur = dim_avg_n_Wrap(slp_cur, 0)
end if

; 获取气候场的平均
f_cli    = addfiles (files_cli, "r")
ListSetType(f_cli, "join")
slp_cli = f_cli[:]->MSL_GDS0_SFC_S123
slp_cli = slp_cli / 100
; printVarSummary(slp)

if dimsizes(files_cli) .eq. 1 then
    ; print(dimsizes(files))
    slp_avg_cli = slp_cli
else
    slp_avg_cli = dim_avg_n_Wrap(slp_cli, 0)
end if

; 求异常场
slp_ano = slp_avg_cli
slp_ano = slp_avg_cur - slp_avg_cli
slp_ano = slp_ano 
slp_ano@long_name = ""
slp_ano@units = ""
slp_avg_cur@long_name = ""
slp_avg_cur@units = ""
; print(min(slp_ano))
; print(max(slp_ano))
wks = gsn_open_wks("png", pic_name)                  ; send graphics to PNG file
res = True
res@gsnDraw           = False    ; Set to False so we can add 
res@gsnFrame          = False    ; shapefile outlines.
res@tmXTOn = False
res@tmYROn = False
res@cnLevelSelectionMode="ExplicitLevels"
print(fspan(980, 1050, 29))
res@cnLevels = fspan(980, 1050, 29)
res@cnMonoLineThickness = False
res@cnLineThicknesses = value
res@cnLineThicknessF=5
res@cnInfoLabelOn=False
res@cnLineColor="black"
res@cnLineLabelInterval=2
res@tiMainString = leftstring
res@tiMainFontHeightF = 0.018
res@tiMainOffsetYF = -0.01
res@cnLineLabelFontHeightF=0.01
plot1 = gsn_csm_contour(wks, slp_avg_cur(::6,::6), res)         ; create a default plot

cnres                             = True
cnres@mpShapeMode = "FreeAspect"
cnres@vpWidthF = 0.8
cnres@vpHeightF = 0.6
cnres@vpXF = 0.1
cnres@vpYF = 0.8
cnres@mpMaxLatF = north
cnres@mpMinLatF = south
cnres@mpMinLonF = west
cnres@mpMaxLonF = east
cnres@gsnMaximize                 = True
cnres@gsnDraw                     = False
cnres@gsnFrame                    = False
cnres@gsnRightString          = ""
cnres@gsnLeftString           = ""  
cnres@gsnStringFontHeightF=15

cnres@cnLinesOn                   = False
cnres@cnLineLabelsOn=False
cnres@cnFillOn                    = True
cnres@cnFillPalette               = "BlueDarkRed18"
cnres@mpFillOn                    = False
cnres@mpGeophysicalLineColor      = "Grey18"
cnres@mpGeophysicalLineThicknessF = 1.5
cnres@tmXTOn = False
cnres@tmYROn = False
cnres@cnLevelSelectionMode="ExplicitLevels"
cnres@cnLevels=ispan(-12, 12, 2)
; cnres@tmYLMode="Explicit"
; cnres@tmYLDataBottomF=-40
; cnres@tmYLDataTopF=60
cnres@lbLabelBarOn        =  True
cnres@gsnAddCyclic                = False
; cnres@tmXBFontHeight=0.05

plot_ano = gsn_csm_contour_map(wks, slp_ano(::4,::4), cnres)   
overlay(plot_ano,plot1)   
draw(plot_ano)
frame(wks)
end