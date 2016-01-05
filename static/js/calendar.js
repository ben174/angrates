$(function() {
    $('.tiny-label').tooltip(
        {
            placement: 'bottom',
        }
    );
    applyDateClasses();
});

function applyDateClasses() {
    $(".date").each(function(i, item) {
        $(item).children(".hours").html().trim() == ''

    });


}