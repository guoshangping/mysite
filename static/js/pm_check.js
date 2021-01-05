function change_cls(obj) {
    if ($(obj).hasClass("layui-form-checked")) {
        $(obj).removeClass("layui-form-checked")
    }
    else {
        $(obj).addClass("layui-form-checked");
    }
}
