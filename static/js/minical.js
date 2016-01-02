
$(function() {
    var calUrl = $("#minical").attr("data-src");
    $.get('/minical' + calUrl, function(data) {
        $("#minical").html(data);
        $("#minical div.calpager a").click(miniCalPage);
    });
});

function miniCalPage(e) {
    var url = $(e.target).closest('a').attr('href');
    $("#minical").fadeOut(100);
    $.get('/minical' + url, function(data) {
        $("#minical").html(data);
        $("#minical div.calpager a").click(miniCalPage);
        $("#minical").fadeIn(100);
    });
    return false;
}