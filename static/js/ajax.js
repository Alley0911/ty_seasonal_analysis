var btn = $("button")[0];
var drawing = $(".drawing")[0]
var pic_result = $(".pic_result")[0]
var pic_temp = $(".pic")[0]


btn.onclick = function(){
    var data_selected = $(".data_name")[0].innerText;
    var var_selected = $("input[name='var_type']:checked").val();
    var level_selected = $("input[name='level_type']:checked").val();
    var start_year_selected = $("#start_year option:selected").val();
    var start_month_selected = $("#start_month option:selected").val();
    var end_year_selected = $("#end_year option:selected").val();
    var end_month_selected = $("#end_month option:selected").val();

    var north = document.getElementById("north").value;
    var south = document.getElementById("south").value;
    var east = document.getElementById("east").value;
    var west= document.getElementById("west").value;


    // 让绘图中的gif显示
    drawing.style.display = "block"

    // 创建ajax对象
    var xhr = new XMLHttpRequest();
    // 配置ajax对象
    var params = 'data=' + data_selected
    params = params + "&var=" + var_selected
    params = params + "&level=" + level_selected
    params = params + "&start_year=" + start_year_selected
    params = params + "&start_month=" + start_month_selected
    params = params + "&end_year=" + end_year_selected
    params = params + "&end_month=" + end_month_selected
    params = params + "&east=" + east
    params = params + "&west=" + west
    params = params + "&north=" + north
    params = params + "&south=" + south
    console.log(params)
    xhr.open('get', 'http://192.168.0.2:5000/draw_pic?' + params)
    // 发送请求
    // xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.send();
    // 获取服务器端响应的数据
    xhr.onload = function () {
        drawing.style.display = "none"
        pic_temp.style.display = "none"
        pic_result.style.backgroundImage = "url(http://192.168.0.2:5000/draw_pic?"+params+")"
        pic_result.style.display = 'block'
    }
}
