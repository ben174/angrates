$(function() {
    $('.tiny-label').tooltip(
        {
            placement: 'bottom',
        }
    );
    applyDateClasses();
    if($("div.hours>a").length==0) {
        $("#alt-notice").removeClass("hidden");
    }
});

function applyDateClasses() {
    $(".date").each(function(i, item) {
        $(item).find(".hours").html().trim() == ''

    });


}