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
data = (args(8))
var = (args(9))
leftstring = (args(10))
filepath = "/home/alley/data/ERA5_monthly/SST/"
number = (end_year - start_year + 1) * (end_month - start_month +1)
files = new(number, string)
n = 0
pic_name = "/home/alley/work/tyanalyse/project/local_pic/result"
do y = start_year, end_year
    do m = start_month, end_month
        if (m .le. 9) then
            files(n) = filepath + "sst_" + y + "0" + m + ".nc"
        else
            files(n) = filepath + "sst_" + y + m + ".nc"
        end if
        n = n + 1
    end do
end do
; print(files)
f    = addfiles (files, "r")
ListSetType(f, "join")
sst = f[:]->SSTK_GDS0_SFC_S123
; printVarSummary(sst)
sst = sst - 273.15

if dimsizes(files) .eq. 1 then
    ; print(dimsizes(files))
    sst_avg = sst
else
    sst_avg = dim_avg_n_Wrap(sst, 0)
end if
sst_avg@long_name = ""
sst_avg@units = ""

wks = gsn_open_wks("png", pic_name)
res                     =  True
res@gsnMaximize         =  True         ;-- maximize plots
res@cnFillOn            =  True         ;-- contour fill
res@cnLinesOn           =  False
res@cnLineLabelsOn      =  False
res@mpMaxLatF = north
res@mpMinLatF = south
res@mpMaxLonF = east
res@mpMinLonF = west
res@tiMainString = leftstring
res@cnFillPalette       = "BlueDarkRed18"     ;-- choose color map
res@mpProjection        = "Robinson"  
res@mpGridAndLimbOn     =  False         ;-- draw grid lines
res@mpCenterLonF        =  150
res@lbLabelBarOn        =  True        ;-- don't draw a labelbar
res@cnLevelSelectionMode = "ManualLevels"
res@cnMinLevelValF      = 15
res@cnMaxLevelValF      = 30
res@cnLevelSpacingF     = 1
plot = gsn_csm_contour_map(wks,sst_avg,res)
end