$(".arrowleft--index").click(function () {
    $(".nav--people").addClass("movetocenter");

    $(".nav--home").addClass("movetoright");
})

$(".arrowright--index").click(function () {
    $(".nav--companies").addClass("movetocenter");

    $(".nav--home").addClass("movetoleft");
})

//People

$(".arrowright--people").click(function () {
    $(".nav--people").removeClass("movetocenter");
    $(".nav--home").removeClass("movetoright");
})


//Companies

$(".arrowleft--companies").click(function () {
    $(".nav--companies").removeClass("movetocenter");
    $(".nav--home").removeClass("movetoleft");
})


//animation viewinfo

$(".item-info-one").hover(function () {
    $(".item-info__img-one").addClass("jello-vertical");
    $(".item-info__img-two").removeClass("jello-vertical");
    $(".item-info__img-three").removeClass("jello-vertical");

    $(".item-info__text-one").addClass("item-info__text--scale");
    $(".item-info__text-two").removeClass("item-info__text--scale");
    $(".item-info__text-three").removeClass("item-info__text--scale");

    $(".item-info__title-one").addClass("item-info__title-one--paint");

})

$(".item-info-two").hover(function () {
    $(".item-info__img-two").addClass("jello-vertical");
    $(".item-info__img-one").removeClass("jello-vertical");
    $(".item-info__img-three").removeClass("jello-vertical");

    $(".item-info__text-two").addClass("item-info__text--scale");
    $(".item-info__text-one").removeClass("item-info__text--scale");
    $(".item-info__text-three").removeClass("item-info__text--scale");

    $(".item-info__title-two").addClass("item-info__title-two--paint");
})

$(".item-info-three").hover(function () {
    $(".item-info__img-three").addClass("jello-vertical");
    $(".item-info__img-two").removeClass("jello-vertical");
    $(".item-info__img-one").removeClass("jello-vertical");

    $(".item-info__text-three").addClass("item-info__text--scale");
    $(".item-info__text-two").removeClass("item-info__text--scale");
    $(".item-info__text-one").removeClass("item-info__text--scale");

    $(".item-info__title-three").addClass("item-info__title-three--paint");
})



//Share animation

$(function(){
  var flag=0;

  $('.share').on('click',function(){
   if(flag == 0)
    {
      $(this).siblings('.one').animate({
      top:'-80px',
      left:'50%',
    },150);

     $(this).siblings('.two').delay(200).animate({
      top:'-30px',
      left:'45%'
    },150);

     $(this).siblings('.three').delay(300).animate({
      top:'-30px',
      left:'55%'
    },150);

    $('.one i,.two i, .three i').delay(500).fadeIn(200);
      flag = 1;
    }


  else{
    $('.one, .two, .three').animate({
        top:'-5px',
        left:'50%'
      },100);

  $('.one i,.two i, .three i').delay(500).fadeOut(200);
      flag = 0;
    }
  });
});

//menu animation

$(".button_menu").click(function () {
    $(".main--profile").toggleClass("main--menuvisible")
    $(".menu").toggleClass("menu--visible")
    $(".button_menu-item1").toggleClass("button_menu-item1--view")
    $(".button_menu-item2").toggleClass("button_menu-item2--view")
    $(".button_menu-item3").toggleClass("button_menu-item3--view")
})

