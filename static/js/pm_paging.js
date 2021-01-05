function change_page(obj, url, cr_token) {
    let user_name = "";
    let current_page = 1;
    if (obj != "") {
        if ($("#query_username").html() || $("#query_username").val()) {
            user_name = $("#query_username").val().replace(/(^\s*)|(\s*$)/g, "");
        }
    }
    if (obj != "1" && obj != "") {
        current_page = $(obj).text().replace(/(^\s*)|(\s*$)/g, "");
    }
    if (current_page == "首页") {
        current_page = 1
    }
    if (current_page == "末页") {
        current_page = parseInt(page_vue.total_page)
    }
    if (current_page == "上一页") {
        if (parseInt(page_vue.curr_page) != 1) {
            current_page = parseInt(page_vue.curr_page) - 1;
        }
        else {
            current_page = 1;
        }
    }
    if (current_page == "下一页") {
        if (parseInt(page_vue.curr_page) != page_vue.total_page) {
            current_page = parseInt(page_vue.curr_page) + 1;
        }
        else {
            current_page = page_vue.total_page;
        }
    }
    current_page = parseInt(current_page);
    let request_dic = {"csrfmiddlewaretoken": cr_token, "current_page": current_page};
    if (url == '/xuanxing/user_manage/') {
        let msg_num = $("#pg_num option:selected").val();
        request_dic = {
            "csrfmiddlewaretoken": cr_token,
            "username": user_name,
            "current_page": current_page,
            "msg_num": msg_num
        }
    }
    if (url == '/xuanxing/task_manage/') {
        let msg_num = $("#pg_num option:selected").val();
        request_dic = {
            "csrfmiddlewaretoken": cr_token,
            "current_page": current_page,
            "pj_speed": $("#pj_speed").find("option:selected").val(),
            "deal_user": $("#deal_user").find("option:selected").val(),
            "members": $("#members").find("option:selected").val(),
            "start": $("#start").val(),
            "pj_name": $("#pj_name").val(),
            "msg_num": msg_num,
        }
    }
    if (url == '/xuanxing/log/') {
        let msg_num = $("#msg_num option:selected").val();
        if (isNaN(msg_num) || msg_num == "") {
            msg_num = 8
        }
        request_dic["msg_num"] = msg_num;
    }
    if (url == "/xuanxing/test_anli/") {
        let doc_name = $("#doc_name_id").find("option:selected").val();
        let pj_name = $("#project_id option:selected").text();
        let msg_num = $("#pg_num option:selected").val();
        request_dic["doc_name"] = doc_name;
        request_dic["pj_name"] = pj_name;
        request_dic["msg_num"] = msg_num
    }
    if (url == '/xuanxing/project_daily/') {
        request_dic["pj_id"] = $("#project_name").find("option:selected").val();
        let msg_num = $("#pg_num option:selected").val();
        request_dic["msg_num"] = msg_num
    }

    $.ajax({
        url: url,
        type: 'post',
        data: request_dic,
        success: function (msg) {
            let ReState = eval("(" + JSON.stringify(msg) + ")");
            if (ReState["code"] == "0000") {
                page_vue.$set(page_vue, "current_list", ReState["data"]);
                page_vue.$set(page_vue, "total_page", ReState["total_page"]);
                page_vue.$set(page_vue, "curr_page", ReState["curr_page"]);
                page_vue.$set(page_vue, "page_jizhun", ReState["page_jizhun"]);
                let box_style = page_vue.box_style;
                let select_flag = page_vue.select_flag;
                if (url == "/xuanxing/task_manage/" || url == "/xuanxing/test_anli/") {
                    let curr_data = ReState["data"];
                    for (let dt_index in curr_data){
                         let dt_id = curr_data[dt_index]["id"].toString();
                         if (!box_style.hasOwnProperty(dt_id)){
                             // 没露面的 如果全选选中的情况 就把没露面的置为全选中， 已经露过面的不用管
                             if (select_flag == 1){
                                 box_style[dt_id] = {box_active: true}
                             }
                             else {
                                 box_style[dt_id] = {box_active: false}
                             }
                         }
                    }
                    page_vue.$set(page_vue, "box_style", box_style);
                }
                if (ReState["url"] == "task_manage") {
                    page_vue.$set(page_vue, "user_list", ReState["user_list"]);
                    page_vue.$set(page_vue, "sp_obj", ReState["sp_obj"]);
                    page_vue.$set(page_vue, "value1", ReState["value1"]);
                    page_vue.$set(page_vue, "value2", ReState["value2"]);
                    page_vue.$set(page_vue, "value3", ReState["value3"]);
                }
                // [0,1,1]  第1个值代表页码数值，第2个值(0:span标签,1:a标签) 第3个值(1:当前页,0:非当前页)
                current_page = parseInt(ReState["curr_page"]);
                let total_page = parseInt(ReState["total_page"]);
                if (current_page > total_page) {
                    current_page = total_page;
                }
                if (total_page == 1) {
                    page_vue.$set(page_vue, "page_list", [["首页", 0, 0], [1, 0, 1]]);
                }
                if (total_page > 1 && total_page < 7) {
                    let page_list_all = [["首页", 1, 0], ["上一页", 1, 0]];
                    for (let i = 1; i < total_page + 1; i++) {
                        if (i == 1 && i == current_page) {
                            page_list_all[0] = ["首页", 0, 0];
                            page_list_all.push([i, 0, 1])
                        }
                        else {
                            if (i != current_page) {
                                page_list_all.push([i, 1, 0])
                            }
                            else {
                                page_list_all.push([i, 0, 1])
                            }
                        }
                    }
                    page_list_all.push(["下一页", 1, 0]);
                    page_list_all.push(["末页", 1, 0]);
                    page_vue.$set(page_vue, "page_list", page_list_all);
                }
                if (total_page >= 7) {
                    let page_list_all = [["首页", 1, 0], ["上一页", 1, 0]];
                    if (current_page < 4) {
                        for (let i = 1; i < 5; i++) {
                            if (i == 1 && i == current_page) {
                                page_list_all[0] = ["首页", 0, 0];
                                page_list_all.push([i, 0, 1])
                            }
                            else {
                                if (i != current_page) {
                                    page_list_all.push([i, 1, 0])
                                }
                                else {
                                    page_list_all.push([i, 0, 1])
                                }
                            }
                        }
                        page_list_all.push(["...", 0, 0]);
                        page_list_all.push([total_page, 1, 0]);
                    }
                    else {
                        let start = current_page - 2;
                        let end = current_page + 2;
                        if (end > total_page) {
                            end = total_page
                        }
                        for (let i = start; i < (end + 1); i++) {
                            if (i != current_page) {
                                page_list_all.push([i, 1, 0])
                            }
                            else {
                                page_list_all.push([i, 0, 1])
                            }
                        }
                        if ((current_page + 2) < total_page) {
                            if ((current_page + 3) < total_page) {
                                page_list_all.push(["...", 0, 0])
                            }
                            page_list_all.push([total_page, 1, 0])
                        }
                    }
                    page_list_all.push(["下一页", 1, 0]);
                    page_list_all.push(["末页", 1, 0]);
                    page_vue.$set(page_vue, "page_list", page_list_all);
                }

                return false;
            } else if (ReState["code"] == "0004") {
                layer.msg("提交失败");
                return false;
            } else if (ReState["code"] == "0003") {
                alert("提交失败2")
            }
        }
    });
}
