$(function() {
    $("div.listen>a").click(linkToPlayer);
});

function linkToPlayer(e) {
    var link = $(e.target).attr('href');
    var src = $("<source>").attr({
        src: link,
        type: "audio/mpeg",
    });
    var audio = $("<audio controls>").attr('autoplay', 'true').append(src).bind('ended', playNext);
    $(e.target).replaceWith(audio);
    return false;
}

function playNext(e) {
    var primary = $(e.target).index() == '0';
    $(e.target).closest(".row.hour").next().find("a.btn-"+(primary?"primary":"default")).click();
}