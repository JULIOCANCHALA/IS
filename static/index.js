
//Change of height on main of home
$(document).ready(function($){
	//var ventana_ancho = $(window).width();
    $('html,body').animate({
        scrollTop: $(".main-one").offset().top},400);
	var windows_height = $(window).height();
	$(".main--home").css("height", windows_height);
	$(".main-one").addClass("main--visible");
});

//scroll animation in main
$(".main__selector-one").click(function() {
    $('html,body').animate({scrollTop: $(".main-one").offset().top},100);
    $(".main-one").addClass("main--visible");
    $(".main-two").removeClass("main--visible");
    $(".main-three").removeClass("main--visible");
});


$(".main__selector-two").click(function() {
    $('html,body').animate({scrollTop: $(".main-two").offset().top},100);
    $(".main-one").removeClass("main--visible");
    $(".main-two").addClass("main--visible");
    $(".main-three").removeClass("main--visible");
});

$(".main__selector-three").click(function() {
    $('html,body').animate({scrollTop: $(".main-three").offset().top},100);
    $(".main-one").removeClass("main--visible");
    $(".main-two").removeClass("main--visible");
    $(".main-three").addClass("main--visible");
});




$(window).bind('mousewheel', function(event) {
    if (event.originalEvent.wheelDelta >= 0) {
        //console.log('Scroll up');
        if($(window).scrollTop()>=$(window).height()  && $(window).scrollTop()<($(window).height())*2 ) {
            $('html,body').animate({scrollTop: $(".main-one").offset().top},100,"linear");
            $(".main-one").addClass("main--visible");
            $(".main-two").removeClass("main--visible");
        }
        if($(window).scrollTop()>=($(window).height())*2 ) {
            $('html,body').animate({scrollTop: $(".main-two").offset().top},100,"linear");
            $(".main-two").addClass("main--visible");
            $(".main-three").removeClass("main--visible");
        }
    }
    else {
        //console.log('Scroll down');
        if($(window).scrollTop()>=0  && $(window).scrollTop()<$(window).height() ) {
            $('html,body').animate({scrollTop: $(".main-two").offset().top},100,"linear");
            $(".main-one").removeClass("main--visible");
            $(".main-two").addClass("main--visible");
        }
        if($(window).scrollTop()>=$(window).height()  && $(window).scrollTop()<($(window).height())*2 ) {
            $('html,body').animate({scrollTop: $(".main-three").offset().top},100,"linear");
            $(".main-three").addClass("main--visible");
            $(".main-two").removeClass("main--visible");
        }
    }
});


$(window).keyup(function(e){
    switch(e.which) {
        case 38: // up
            if($(window).scrollTop()>=$(window).height()  && $(window).scrollTop()<($(window).height())*2 ) {
                $('html,body').animate({scrollTop: $(".main-one").offset().top},100,"linear");
                $(".main-one").addClass("main--visible");
                $(".main-two").removeClass("main--visible");
            }
            if($(window).scrollTop()>=($(window).height())*2 ) {
                $('html,body').animate({scrollTop: $(".main-two").offset().top},100,"linear");
                $(".main-two").addClass("main--visible");
                $(".main-three").removeClass("main--visible");
            }

        break;

        case 40: // down
            if($(window).scrollTop()>=0  && $(window).scrollTop()<$(window).height() ) {
                $('html,body').animate({scrollTop: $(".main-two").offset().top},100,"linear");
                $(".main-one").removeClass("main--visible");
                $(".main-two").addClass("main--visible");
            }
            if($(window).scrollTop()>=$(window).height()  && $(window).scrollTop()<($(window).height())*2 ) {
                $('html,body').animate({scrollTop: $(".main-three").offset().top},100,"linear");
                $(".main-three").addClass("main--visible");
                $(".main-two").removeClass("main--visible");
            }

        break;

        default: return; // exit this handler for other keys
    }
    e.preventDefault(); // prevent the default action (scroll / move caret)

});
