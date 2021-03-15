laydate.render({
    elem: '#start_time_year_month', //指定元素
    type: 'month'
    ,min: '1981-1-1'
    ,max: '2021-2-1'
    ,btns: ['clear', 'confirm']
    ,value: '1981-01'
});
laydate.render({
    elem: '#end_time_year_month', //指定元素
    type: 'month'
    ,min: '1981-1-1'
    ,max: '2021-2-1'
    ,btns: ['clear', 'confirm']
    ,value: '2020-12'
});
laydate.render({
    elem: '#start_time_year_month_day'
    ,type: "date"
    ,min: '2017-1-1'
    ,max: '2020-12-31'
    ,btns: ['clear', 'confirm']
    ,value: '2017-01-01'
});
laydate.render({
    elem: '#end_time_year_month_day'
    ,type: "date"
    ,min: '1981-1-1'
    ,max: '2020-12-31'
    ,btns: ['clear', 'confirm']
    ,value: '2020-12-31'
});
//根据data_type.json动态生成不同数据类型的数据菜单栏的头部
$.get("../static/json/data_type.json", function(data){
        for(var i in data){
            id = data[i].data_type;
            ch_name = data[i].ch_name;
            append_tmp="<ul class='top_menu_title' id='"+id+"'><li>"+ch_name+"</li></ul>";
            // console.log(append_tmp)
            $(".top_menu_box").append(append_tmp);
        }
    });

// 根据data.json动态生成不同数据类型的数据列表
$.get("../static/json/data_type.json", function(data){
        for(var i in data){
            index = data[i].data_type;
            // console.log(index)
            data_list = data[i].data_list;
            for (var j in data_list){
                data_tmp = data_list[j]
                append_tmp="<li class='top_menu_list'>"+data_tmp+"</li>"
                $("#"+index).append(append_tmp)
            }
        }
    });

// 鼠标经过显示菜单title后变色，并显示data_list
$('.top_menu_box').on('mouseover', ".top_menu_title", function () {
    //变色
    $(this).css({'cursor': 'pointer', 'background-color': 'whitesmoke'});
    //显示
    li_tmp = ($(this).children());
    li_tmp[0].style.color='#14539a';
    // console.log(li_tmp.length)
    for(var i=1; i<li_tmp.length;i++){
        li_tmp[i].style.display='block'
    }
});
//
// 鼠标离开显示菜单title后变色，并不显示data_list
$('.top_menu_box').on('mouseout', ".top_menu_title", function () {
    $(this).css({'background-color':'#2d97db'})
    li_tmp = ($(this).children());
    // console.log(li_tmp.length)
    li_tmp[0].style.color='black';
    for(var i=1; i<li_tmp.length;i++){
        li_tmp[i].style.display='none'
    }
});

// 鼠标经过子数据时，样式变换
$('.top_menu_box').on('mouseover', ".top_menu_title", function () {
    //变色
    $(this).css({'cursor': 'pointer', 'background-color': 'whitesmoke'});
    //显示
    li_tmp = ($(this).children());
    li_tmp[0].style.color='#14539a';
    // console.log(li_tmp.length)
    for(var i=1; i<li_tmp.length;i++){
        li_tmp[i].style.display='block'
    }
});

// 鼠标离开显示菜单title后变色，并不显示data_list
$('.top_menu_box').on('mouseover', ".top_menu_list", function () {
    $(this).css({'font-weight':'800','text-decoration':'underline'})
});

// 鼠标离开子数据时，样式变换
$('.top_menu_box').on('mouseout', ".top_menu_list", function (){
    $(this).css({'font-weight':'400','text-decoration':'none'})
});

//在页面打开时先默认生成ERA5_Monthly的var_list，后续根据需要在进行在自动修改
$.get('../static/json/var_list.json', function(data){
    for (var i in data){
        if (data[i].data_name == 'ERA5_Monthly'){
        if (i==0){
            append_tmp = "<option selected='selected' value=" +data[i].var_en_name+">"+data[i].var_cn_name+"</option>"
        }
        else {
            append_tmp = "<option value=" +data[i].var_en_name+">"+data[i].var_cn_name+"</option>"
        }

        $(".var_list").append(append_tmp)
        }
    }
})

//在页面打开时默认生成年月类型的laydate实例，起止日期为1981-1-1至2020-12-31
//后续改变变量和数据类型时，laydate都应该自动有所调整


//鼠标点击data_list之后
// 0.下部内容区的左侧头部的数据名更改
// 1.生成相应的变量列表，并将第一个默认选中
// 2.隐藏该菜单
// 3.清除level所有的option并恢复默认的无定义状态
// 4.生成对应时间格式,需要先删除再重新生成
// 5.如果是台风数据则不显示图形区域
$('.top_menu_box').on('click', ".top_menu_list", function () {

    var data_selected = ($(this).text());

    //0.下部内容区的左侧头部的数据名更改
    $("div.data_name").html(data_selected)

    //5.如果是台风数据则不显示图形区域，其他数据都显示图形区域
    if (data_selected=="CMA"){
        $(".location_box").css("display","none")
    }
    else{
        $(".location_box").css("display","block")
    }

    // var bro_li = ($(this).siblings()); //返回兄弟节点单不包括自己
    var li_tmp = ($(this).parent().children()); //返回父节点的子节点即自己和所有兄弟节点

    //隐藏子菜单，子菜单是从第二个li开始的
    for(var i=1; i<li_tmp.length;i++){
        li_tmp[i].style.display='none'
    }

    //根据var_list.json写入分析的变量列表
    //生成对应的变量列表，生成前需要先删除所有的var_list
    $(".var_list").find('option').remove() //删除所有已有的var_list
    $.get('../static/json/var_list.json', function(data){
        var j = 0 //如果是添加的第一个将被默认选中
        for (var i in data){
            if (data_selected == data[i].data_name){
                // time_type_selected = data[i].time_type;
                // console.log(time_type_selected)
                // start_time = data[i].start_time
                // end_time = data[i].end_time

                if (j==0){
                    append_tmp = "<option selected='selected' value=" +data[i].var_en_name+">"+data[i].var_cn_name+"</option>"
                }
                else {
                    console.log(123);
                    append_tmp = "<option value=" +data[i].var_en_name+">"+data[i].var_cn_name+"</option>"
                }
                $(".var_list").append(append_tmp)
                j = j + 1
            }
        }
    })
    function get_selected_others_from_data_type(selected,cb){
        $.get('../static/json/data.json', function(data){
            for (var i in data){
                if (selected == data[i].data_name){
                    var time_type_selected = data[i].time_type;
                    var start_time = data[i].start_time
                    var end_time = data[i].end_time
                    cb([time_type_selected, start_time, end_time])
                }
            }
        })
    }

    // 3.清除level所有的option并恢复默认的无定义状态
    $(".level_list").find("option").remove();
    append_tmp = "<option value=\"none\"  selected = \"selected\" >无定义</option>"
    $(".level_list").append(append_tmp)

    //4.生成相应的时间格式
    get_selected_others_from_data_type(data_selected,function (data) {
        var time_type_selected = data[0]
        var start_time = data[1]
        var end_time = data[2]
        // console.log(time_type_selected)
        // console.log(start_time)
        // console.log(end_time)
        if (time_type_selected == 'year_month'){
            ($('#month_start').children('input').remove());
            ($('#month_end').children('input').remove());
            $("#month_start").append("<input type=\"text\" class=\"month\" id=\"start_time_year_month\">")
            $("#month_end").append("<input type=\"text\" class=\"month\" id=\"end_time_year_month\">")
            $("div.year_month").css('display','block');
                $("div.year_month_day").css('display','none');
                laydate.render({
                    elem: '#start_time_year_month', //指定元素
                    type: 'month'
                    ,min: start_time
                    ,max: end_time
                    ,btns: ['clear', 'confirm']
                    ,value: start_time.substring(0,7)
                });
                laydate.render({
                    elem: '#end_time_year_month', //指定元素
                    type: 'month'
                    ,min: start_time
                    ,max: end_time
                    ,btns: ['clear', 'confirm']
                    ,value: end_time.substring(0,7)
                });
            }
        if (time_type_selected == 'year_month_day'){
            ($('#date_start').children('input').remove());
            ($('#date_end').children('input').remove());
            $("#date_start").append("<input type=\"text\" class=\"date\" id=\"start_time_year_month_day\">")
            $("#date_end").append("<input type=\"text\" class=\"date\" id=\"end_time_year_month_day\">")
            $("div.year_month_day").css('display','block');
            $("div.year_month").css('display','none');
            laydate.render({
                elem: '#start_time_year_month_day'
                ,min: start_time
                ,max: end_time
                ,btns: ['clear', 'confirm']
                ,value: start_time
            });
            laydate.render({
                elem: '#end_time_year_month_day'
                ,min: start_time
                ,max: end_time
                ,btns: ['clear', 'confirm']
                ,value: end_time
            });
        }
    })
});

// 要获取动态添加的option:selected选项，change事件使得点击动态添加的默认选项时无法触发事件，因此选择click事件绑定
$(".var_list").change(function(){
    var_selected = ($(".var_list").val())
});

// 绑定变量列表的click事件
// 1.用于获取动态添加的option事件从而动态改变level的值
// 2.同时根据var的值改变时间的值
$('.var_list').click(function () {
    var var_selected = ($(this).val())
    // console.log(var_selected);

    //1. 动态改变level的值
    $.get("../static/json/var_list.json", function(data){
        for(var i in data){
            var tmp_var = data[i].var_en_name;
            if(var_selected == tmp_var){
                $(".level_list").find("option").remove();
                value_tmp = data[i].level_code;
                text_tmp = data[i].level;
                // console.log(value_tmp);
                // console.log(text_tmp);
                for(var j=0; j<value_tmp.length;j++){
                    if(j==0){
                        append_tmp = `<option selected='selected' value=${value_tmp[j]}>${text_tmp[j]}</option>`
                    }
                    else{
                        append_tmp = `<option value=${value_tmp[j]}>${text_tmp[j]}</option>`
                    }

                    $(".level_list").append(append_tmp)
                }

            }
        }
    })

    //2. 动态改变时间的起止日期范围
    //3. 用于获取已知的var对应的起止时间的函数,需要先删除再重新生成
    function get_selected_others_from_var_list(selected,cb){
        $.get('../static/json/var_list.json', function(data){
            for (var i in data){
                if (selected == data[i].var_en_name){
                    var time_type_selected = data[i].time_type;
                    var start_time = data[i].start_time
                    var end_time = data[i].end_time
                    cb([time_type_selected, start_time, end_time])
                }
            }
        })
    }
    get_selected_others_from_var_list(var_selected, function (data) {

        var time_type_selected = data[0]
        var start_time = data[1]
        var end_time = data[2]
        if (time_type_selected == 'year_month'){
                ($('#month_start').children('input').remove());
                ($('#month_end').children('input').remove());
                $("#month_start").append("<input type=\"text\" class=\"month\" id=\"start_time_year_month\">")
                $("#month_end").append("<input type=\"text\" class=\"month\" id=\"end_time_year_month\">")
                $("div.year_month").css('display','block');
                $("div.year_month_day").css('display','none');
                laydate.render({
                    elem: '#start_time_year_month', //指定元素
                    type: 'month'
                    ,min: start_time
                    ,max: end_time
                    ,btns: ['clear', 'confirm']
                    ,value: start_time.substring(0,7)
                });
                laydate.render({
                    elem: '#end_time_year_month', //指定元素
                    type: 'month'
                    ,min: start_time
                    ,max: end_time
                    ,btns: ['clear', 'confirm']
                    ,value: end_time.substring(0,7)
                });
            }
        if (time_type_selected == 'year_month_day'){
            ($('#date_start').children('input').remove());
            ($('#date_end').children('input').remove());
            $("#date_start").append("<input type=\"text\" class=\"date\" id=\"start_time_year_month_day\">")
            $("#date_end").append("<input type=\"text\" class=\"date\" id=\"end_time_year_month_day\">")
            $("div.year_month_day").css('display','block');
            $("div.year_month").css('display','none');
            laydate.render({
                elem: '#start_time_year_month_day'
                ,min: start_time
                ,max: end_time
                ,btns: ['clear', 'confirm']
                ,value: start_time
            });
            laydate.render({
                elem: '#end_time_year_month_day'
                ,min: start_time
                ,max: end_time
                ,btns: ['clear', 'confirm']
                ,value: end_time
            });
        }
    })
});


// $('.submit').click(function () {
//     var_selected = ($(".var_list").val())  // 变量名
//     data_selected = ($("div.data_name").text())
//     console.log(data_selected)
//     console.log(var_selected)
//     console.log($("div.year_month").css('display'))
// })
