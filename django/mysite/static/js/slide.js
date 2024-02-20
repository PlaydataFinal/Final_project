$(function () {
    $('.btn_play').click(function () {
        // [재생] 버튼을 클릭하면 -webkit-animation-play-state: running 속성 적용
        if ($('.original').css('animation-play-state') == 'paused') {
            $('.original').css('animation-play-state', 'running');
            $('.clone').css('animation-play-state', 'running');
            $('.play_btn').css('src', "https://thumb.silhouette-ac.com/t/6b/6b13895a4c75e2b38ea58534e8ab1f6c_t.jpeg");
        }
        else {
            $('.original').css('animation-play-state', 'paused');
            $('.clone').css('animation-play-state', 'paused');
            $('.play_btn').css('src', "https://png.pngtree.com/element_our/20190528/ourmid/pngtree-play-icon-image_1128351.jpg");
        }
    });
});