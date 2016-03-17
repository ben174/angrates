var Player = function() {
    return {
        player: null,
        init: function () {
            console.log(this.player);
            this.player = $("<div>").attr("id", "player").append('<i class="fa fa-play-circle-o"></i>');
            console.log(this.player);
            $("body").append(this.player);
        },
        play: function () {

        }
    };
};


$(function() {
    var player = new Player();
    player.init();
});

