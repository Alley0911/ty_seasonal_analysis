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
level = (args(11))
filepath = "/home/alley/data/" + data + "/UV/"
number = (end_year - start_year + 1) * (end_month - start_month +1)

pic_name = "/home/alley/work/tyanalyse/project/local_pic/result"
files = new(number, string)
n = 0
do y = start_year, end_year
    do m = start_month, end_month
        if (m .le. 9) then
            files(n) = filepath + "uv_" + level + "_" + y + "0" + m + ".grb"
        else
            files(n) = filepath + "uv_" + level + "_" + y + m + ".grb"
        end if
        n = n + 1
    end do
end do
print(files)
f    = addfiles (files, "r")
ListSetType(f, "join")

u = f[:]->U_GDS0_ISBL_S123
printVarSummary(u)
if dimsizes(files) .eq. 1 then
    ; print(dimsizes(files))
    u_avg = u
else
    u_avg = dim_avg_n_Wrap(u, 0)
end if
printVarSummary(u_avg)
v = f[:]->V_GDS0_ISBL_S123
; printVarSummary(u)
if dimsizes(files) .eq. 1 then
    ; print(dimsizes(files))
    v_avg = v
else
    v_avg = dim_avg_n_Wrap(v, 0)
end if
speed_avg = u_avg
speed_avg = sqrt(u_avg*u_avg + v_avg*v_avg)
u_avg@long_name = ""
u_avg@units = ""
u_avg@long_name = ""
u_avg@units = ""
v_avg@long_name = ""
v_avg@units = ""
speed_avg@long_name = ""
speed_avg@units = ""

wks  = gsn_open_wks("png",pic_name) ; send graphics to PNG file

cnres                             = True
; cnres@gsnMaximize                 = True
cnres@gsnDraw                     = False
cnres@gsnFrame                    = False
; cnres@gsnRightString          = "m/s"
; cnres@gsnLeftString           = "cli"  
; cnres@gsnStringFontHeightF=20
cmap = read_colormap_file("WhiteBlueGreenYellowRed")
cnres@cnLinesOn                   = False
cnres@cnLineLabelsOn= False
cnres@tmXTOn = False
cnres@tmYROn = False
cnres@mpShapeMode = "FreeAspect"
cnres@vpWidthF = 0.8
cnres@vpHeightF = 0.6
cnres@vpXF = 0.1
cnres@vpYF = 0.8
cnres@cnFillOn                    = True
cnres@cnFillPalette               = cmap(15:,:)
cnres@mpFillOn                    = False
cnres@mpGeophysicalLineColor      = "Grey18"
cnres@mpGeophysicalLineThicknessF = 1.5
cnres@tiMainString = leftstring
; cnres@tiMainFontHeightF = 0.018
; cnres@tiMainOffsetYF = -0.02
cnres@mpMaxLatF = north
cnres@mpMinLatF = south
cnres@mpMinLonF = west
cnres@mpMaxLonF = east
cnres@mpCenterLonF = 150
cnres@lbLabelBarOn        =  True

vcres                         = True
vcres@gsnDraw                 = False
vcres@gsnFrame                = False
; vcres@vcFillArrowsOn          = True
; vcres@tiMainString = leftstring
; vcres@vcRefMagnitudeF         = 10.0             ; define vector ref mag
; vcres@vcRefLengthF            = 0.02             ; define length of vec ref
; vcres@vcMinFracLengthF        = 0.3
; vcres@vcMinDistanceF          = 0.02
; vcres@vcRefAnnoOrthogonalPosF = -0.45
; vcres@vcRefAnnoFontHeightF    = 0.005
; vcres@vcRefAnnoString2On=False
; vcres@vcRefAnnoString1On=False
vcres@vcRefAnnoOn=False
; vcres@vcGlyphStyle="CurlyVector"
vcres@vcLineArrowThicknessF=3
vcres@vcRefAnnoOrthogonalPosF = -1.0             ; move ref vector up
vcres@vcRefMagnitudeF         = 10.0             ; define vector ref mag
vcres@vcRefLengthF            = 0.045            ; define length of vec ref
vcres@vcGlyphStyle            = "CurlyVector"    ; turn on curly vectors
vcres@vcMinDistanceF          = 0.017

;---Draw fully opaque vectors
uv_plot  = gsn_csm_vector(wks,u_avg(::-10,::10),v_avg(::-10,::10),vcres)
spd_plot = gsn_csm_contour_map(wks,speed_avg(::-10,::10),cnres)
overlay(spd_plot,uv_plot)
draw(spd_plot)
frame(wks)
end
