var data_menu_title = document.getElementsByClassName("data_menu_title")
var data_menu_list = document.getElementsByClassName("data_menu_list")
var var_list = document.querySelectorAll(".var_list")
var var_lables = document.getElementsByClassName("var_list_box")[0].getElementsByTagName("label")
var level_lables = document.getElementsByClassName("level_box")[0].getElementsByTagName("p")


for (var i = 0; i < data_menu_title.length; i++) {
    // 菜单栏经过显示子菜单功能
    data_menu_title[i].onmouseover = function () {

        // 菜单栏下面的子菜单
        data_menu_list_current = (this.childNodes[2])
        data_menu_list_current.style.display = "block"
        li = this.getElementsByTagName("li") //表示子菜单的某项

        // 鼠标经过子菜单的某项，该项回变绿颜色
        for (let ii = 0; ii < li.length; ii++) {
            li[ii].onmouseover = function () {
                li[ii].style.backgroundColor = "green";
            }
        }

        // 点击某个数据之后，变量内容会随之更新，并隐藏下拉显示的菜单
        for (let ii = 0; ii < li.length; ii++) {
            li[ii].onclick = function () {
                console.log(li[ii].innerText);
                var data_selected = $(".data_name")[0];
                data_selected.innerText = li[ii].innerText
                for (let i = 0; i < var_list.length; i++) {
                    var_list[i].style.display = "none"     
                }
                for (let i = 0; i < level_lables.length; i++) {
                    level_lables[i].style.display="none"
                }

                index2 =  li[ii].getAttribute("index")
                if(index2 == "era5_monthly"){
                    var_list[0].style.display = "block"
                }

                if(index2 == "ty_cma"){
                    var_list[1].style.display = "block"
                }
                data_menu_list_current.style.display = "none"
            }
        }

        // 鼠标离开子菜单的某项后，颜色恢复之前的样子
        for (let ii = 0; ii < li.length; ii++) {
            li[ii].onmouseout = function () {
                li[ii].style.backgroundColor = " rgb(248, 201, 118)";
            }
        }

    }

    // 鼠标离开数据菜单的头部之后，下拉菜单消失
    data_menu_title[i].onmouseout = function () {
        // this.style.backgroundColor = " rgb(248, 201, 118)"
        data_menu_list_current = (this.childNodes[2])
        data_menu_list_current.style.display = "none"

    }

}


// 点击某个变量后会显示特定的层次
for (let l = 0; l < var_lables.length; l++) {
    var_lables[l].onclick = function(){
        levels = this.childNodes[0].getAttribute("levels")
        for (let i = 0; i < level_lables.length; i++) {
            level_lables[i].style.display="none"

        }
        for (let i = 0; i < levels.length; i++) {
            if(i == 0){
                // console.log(level_lables[levels[i]].childNodes[1].childNodes[0])
                // 默认层次的第一个选项被选中
                level_lables[levels[i]].childNodes[1].childNodes[0].checked = true
            }
            level_lables[levels[i]].style.display="block"
        }
    }
    
}
