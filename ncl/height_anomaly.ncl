load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"  
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"  
;************************************************
begin
args = asciiread("/home/alley/work/tyanalyse/project/ncl/params.txt", -1, "string")
start_year = stringtoint(args(0))
start_month = stringtoint(args(1))
end_year = stringtoint(args(2))
end_month = stringtoint(args(3))
north = stringtoint(args(4))
south = stringtoint(args(5))
west = stringtoint(args(6))
east = stringtoint(args(7))
leftstring = (args(10))
filepath = "/home/alley/data/ERA5_monthly/height/"
pic_name = "/home/alley/work/tyanalyse/project/local_pic/result"

number = (end_year - start_year + 1) * (end_month - start_month +1)
files_cur = new(number, string)
n = 0
do y = start_year, end_year
    do m = start_month, end_month
        if (m .le. 9) then
            files_cur(n) = filepath + "height_" + level + "_" + y + "0" + m + ".nc"
        else
            files_cur(n) = filepath + "height_" + level + "_" + y + m + ".nc"
        end if
        n = n + 1
    end do
end do
print(files_cur)

; 根据时间获取所需要的气候态的文件
number = 30 * (end_month - start_month +1)
files_cli = new(number, string)
n = 0
do y = 1981, 2010
    do m = start_month, end_month
        if (m .le. 9) then
            files_cli(n) = filepath + "height_" + level + "_" + y + "0" + m + ".nc"
        else
            files_cli(n) = filepath + "sst_" + y + m + ".nc"
        end if
        n = n + 1
    end do
end do
print(files_cli)

; 获取目标场的平均
f_cur    = addfiles (files_cur, "r")
ListSetType(f_cur, "join")
sst_cur = f_cur[:]->SSTK_GDS0_SFC_S123
; printVarSummary(sst)

if dimsizes(files_cur) .eq. 1 then
    ; print(dimsizes(files))
    sst_avg_cur = sst_cur
else
    sst_avg_cur = dim_avg_n_Wrap(sst_cur, 0)
end if

; 获取气候场的平均
f_cli    = addfiles (files_cli, "r")
ListSetType(f_cli, "join")
sst_cli = f_cli[:]->SSTK_GDS0_SFC_S123
; printVarSummary(sst)

if dimsizes(files_cli) .eq. 1 then
    ; print(dimsizes(files))
    sst_avg_cli = sst_cli
else
    sst_avg_cli = dim_avg_n_Wrap(sst_cli, 0)
end if

; 求异常场
sst_end = sst_avg_cli
sst_end = sst_avg_cur - sst_avg_cli
sst_end@long_name = ""
sst_end@units = ""


  wks = gsn_open_wks("png","500hPa_cli_2020")                  ; send graphics to PNG file
  res = True
  res@gsnDraw           = False    ; Set to False so we can add 
  res@gsnFrame          = False    ; shapefile outlines.
  res@mpMaxLatF = 60
  res@mpMinLatF = 0
  res@mpMinLonF = 40
  res@mpMaxLonF = 180
  res@tmXTOn = False
  res@tmYROn = False
  res@cnLevelSelectionMode="ExplicitLevels"
  res@cnLevels=ispan(516, 588, 4)
  res@cnMonoLineThickness = False
  res@cnLineThicknesses = value
  res@cnLineThicknessF=5
  res@cnInfoLabelOn=False
  res@cnLineColor="blue"
  res@cnLineLabelInterval=1
  res@cnLineLabelFontHeightF=0.014
  plot1 = gsn_csm_contour_map(wks,h_cli,res)         ; create a default plot
  dir      = "/mnt/g/ncl/GSHHS_shp/"
  filename = "l/GSHHS_l_L1.shp"
  dum  = gsn_add_shapefile_polylines(wks,plot1,dir+filename,True)
  plot2 = gsn_csm_contour_map(wks,h_98,res)         ; create a default plot
  dir      = "/mnt/g/ncl/GSHHS_shp/"
  filename = "l/GSHHS_l_L1.shp"
  dum1  = gsn_add_shapefile_polylines(wks,plot2,dir+filename,True)
  plot3 = gsn_csm_contour_map(wks,h_20,res)         ; create a default plot
  dir      = "/mnt/g/ncl/GSHHS_shp/"
  filename = "l/GSHHS_l_L1.shp"
  dum11  = gsn_add_shapefile_polylines(wks,plot3,dir+filename,True)
; draw(plot1)
; frame(wks)
pnlres                  =  True
; pnlres@gsnPanelLabelBar =  True         ;-- common labelbar
pnlres@gsnPanelXWhiteSpacePercent =  5
; pnlres@gsnPanelMainFontHeightF =  0.020 ;-- text font size
; pnlres
;-- create panel plot
gsn_panel(wks,(/plot1,plot2,plot3/),(/3,1/),pnlres)
end
