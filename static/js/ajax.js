// 点击绘图按钮后，获取一些select的选项
// 动态添加的默认的option选项无法获取，需要绑定事件，这里是绑定的submit按钮事件
var btn = $("button")[0];
btn.onclick = function () {
    var_selected = ($(".var_list").val())  // 变量名
    data_selected = ($("div.data_name").text())
    var start_time_ym_selected = $("#start_time_year_month").val();
    var start_time_ymd_selected = $("#start_time_year_month_day").val();
    var end_time_ym_selected = $("#end_time_year_month").val();
    var end_time_ymd_selected = $("#end_time_year_month_day").val();
    ym_time_display = ($("div.year_month").css('display')) //记录year_month是否为block，是的话获取年月时间的时间否则获取年月日的时间
    console.log(ym_time_display)
    if(ym_time_display=='block'){
        time_type = 'year_month'
        start_time_selected = start_time_ym_selected
        end_time_selected =  end_time_ym_selected
    }
    else{
        time_type = 'year_month_day'
        start_time_selected = start_time_ymd_selected
        end_time_selected =  end_time_ymd_selected
    }
    var level_selected = ($(".level_list").val());
    var north = document.getElementById("north").value;
    var south = document.getElementById("south").value;
    var east = document.getElementById("east").value;
    var west= document.getElementById("west").value;
    console.log(data_selected)
    console.log(var_selected)
    console.log(level_selected)
    console.log(time_type)
    console.log(start_time_selected)
    console.log(end_time_selected)
    console.log(north)
    console.log(south)
    console.log(east)
    console.log(west)


    var drawing = $(".drawing")[0]  //绘图中的div
    var pic = $(".pic")[0]  //展示图片的div
    var img = $("img")[1] //图片的img标签
    // 让绘图中的gif显示
    drawing.style.display = "block"
    pic.style.display = "none"
    // 创建ajax对象
    var xhr = new XMLHttpRequest();
    // 配置ajax对象
    var params = 'data=' + data_selected
    params = params + "&var=" + var_selected
    params = params + "&level=" + level_selected
    params = params + "&time_type=" + time_type
    params = params + "&start_time=" + start_time_selected
    params = params + "&end_time=" + end_time_selected
    params = params + "&east=" + east
    params = params + "&west=" + west
    params = params + "&north=" + north
    params = params + "&south=" + south
    console.log(params)

    xhr.open('get', '/draw_pic?' + params)
    // 发送请求
    // xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.send();
    // 获取服务器端响应的数据
    xhr.onload = function () {
        drawing.style.display = "none"
        pic.style.display = "table-cell"
        img.src = "/draw_pic?"+params
    }
}

// btn.onclick = function(){
//     var data_selected = $(".data_name")[0].innerText;
//     var var_selected = $("input[name='var_type']:checked").val();
//     var level_selected = $("input[name='level_type']:checked").val();
//     var start_year_selected = $("#start_year option:selected").val();
//     var start_month_selected = $("#start_month option:selected").val();
//     var end_year_selected = $("#end_year option:selected").val();
//     var end_month_selected = $("#end_month option:selected").val();
//     var north = document.getElementById("north").value;
//     var south = document.getElementById("south").value;
//     var east = document.getElementById("east").value;
//     var west= document.getElementById("west").value;
//
//

// }
