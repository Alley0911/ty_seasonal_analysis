begin
; 获取相关参数
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
filepath = "/home/alley/data/" + data + "/SST/"
pic_name = "/home/alley/work/tyanalyse/project/local_pic/result"

; 根据时间获取所需要目标场的文件
number = (end_year - start_year + 1) * (end_month - start_month +1)
files_cur = new(number, string)
n = 0
do y = start_year, end_year
    do m = start_month, end_month
        if (m .le. 9) then
            files_cur(n) = filepath + "sst_" + y + "0" + m + ".grb"
        else
            files_cur(n) = filepath + "sst_" + y + m + ".grb"
        end if
        n = n + 1
    end do
end do

; 根据时间获取所需要的气候态的文件
number = 30 * (end_month - start_month +1)
files_cli = new(number, string)
n = 0
do y = 1981, 2010
    do m = start_month, end_month
        if (m .le. 9) then
            files_cli(n) = filepath + "sst_" + y + "0" + m + ".grb"
        else
            files_cli(n) = filepath + "sst_" + y + m + ".grb"
        end if
        n = n + 1
    end do
end do

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

wks = gsn_open_wks("png", pic_name)
res                     =  True
res@tmXTOn = False
res@tmYROn = False
; res@gsnMaximize         =  True         ;-- maximize plots
res@cnFillOn            =  True         ;-- contour fill
res@cnLinesOn           =  False
res@cnLineLabelsOn      =  False
res@mpShapeMode = "FreeAspect"
res@vpWidthF = 0.8
res@vpHeightF = 0.6
res@vpXF = 0.1
res@vpYF = 0.8
res@mpMaxLatF = north
res@mpMinLatF = south
res@mpMaxLonF = east
res@mpMinLonF = west
res@tiMainString = leftstring
res@tiMainOffsetYF = -0.02
res@cnFillPalette       = "BlueDarkRed18"     ;-- choose color map
res@mpGridAndLimbOn     =  False         ;-- draw grid lines
res@mpCenterLonF        =  150
res@lbLabelBarOn        =  True        ;-- don't draw a labelbar
res@cnLevelSelectionMode = "ManualLevels"
res@cnMinLevelValF      = -5
res@cnMaxLevelValF      = 5
res@cnLevelSpacingF     = 1
plot = gsn_csm_contour_map(wks,sst_end,res)
end