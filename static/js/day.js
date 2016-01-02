$(function() {
    $("div.listen>a").click(linkToPlayer);
    if(QueryString.play!=undefined) {
        $("a.btn-primary")[parseInt(QueryString.play)-1].click();
    }

});

function linkToPlayer(e) {
    var link = $(e.target).attr('href');
    var src = $("<source>").attr({
        src: link,
        type: "audio/mpeg",
    });
    var audio = $("<audio controls>").attr('autoplay', 'true').append(src).bind('ended', playNext);
    $('audio').each(function(){
        this.pause();
    });
    $(e.target).replaceWith(audio);
    return false;
}

function playNext(e) {
    var primary = $(e.target).index() == '0';
    $(e.target).closest(".row.hour").next().find("a.btn-"+(primary?"primary":"default")).click();
}


var QueryString = function () {
    // This function is anonymous, is executed immediately and
    // the return value is assigned to QueryString!
    var query_string = {};
    var query = window.location.search.substring(1);
    var vars = query.split("&");
    for (var i = 0; i < vars.length; i++) {
        var pair = vars[i].split("=");
        // If first entry with this name
        if (typeof query_string[pair[0]] === "undefined") {
            query_string[pair[0]] = decodeURIComponent(pair[1]);
            // If second entry with this name
        } else if (typeof query_string[pair[0]] === "string") {
            var arr = [query_string[pair[0]], decodeURIComponent(pair[1])];
            query_string[pair[0]] = arr;
            // If third or later entry with this name
        } else {
            query_string[pair[0]].push(decodeURIComponent(pair[1]));
        }
    }
    return query_string;
}();