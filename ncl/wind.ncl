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
level = stringtoint(args(11))
filepath = "/home/alley/data/ERA5_monthly/UV/"
number = (end_year - start_year + 1) * (end_month - start_month +1)

files = new(number, string)
n = 0
pic_name = "/home/alley/work/tyanalyse/project/local_pic/result"
do y = start_year, end_year
    do m = start_month, end_month
        if (m .le. 9) then
            files(n) = filepath + "uv_850_200_" + y + "0" + m + ".nc"
        else
            files(n) = filepath + "uv_850_200_" + y + m + ".nc"
        end if
        n = n + 1
    end do
end do
; print(files)
f    = addfiles (files, "r")
ListSetType(f, "join")

u = f[:]->u(:,0,{level},:,:)
v = f[:]->v(:,0,{level},:,:)

u_avg_tmp = dim_avg_n_Wrap(u, 0)  
v_avg_tmp = dim_avg_n_Wrap(v, 0)
u_avg = u_avg_tmp * u@scale_factor + u@add_offset
v_avg = v_avg_tmp * v@scale_factor + v@add_offset
speed_avg = sqrt(u_avg*u_avg + v_avg*v_avg)
copy_VarCoords(u_avg_tmp, u_avg)
copy_VarCoords(v_avg_tmp, v_avg)
copy_VarCoords(u_avg_tmp, speed_avg)
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
cnres@cnFillOn                    = True
cnres@cnFillPalette               = cmap(15:,:)
cnres@mpFillOn                    = False
cnres@mpGeophysicalLineColor      = "Grey18"
cnres@mpGeophysicalLineThicknessF = 1.5
cnres@tiMainString = leftstring
cnres@tiMainOffsetYF = -0.015
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