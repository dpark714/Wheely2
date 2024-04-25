$(document).ready(function () {
    ////////////////////////////////////////
    // Back to top
    ////////////////////////////////////////

    var scroll_speed = 800;

    if( $('#back-to-top').length ){

        $('#back-to-top > a').click(function() {
            $('body, html').animate({
                scrollTop: 0
            }, scroll_speed );
        });

        $(window).scroll(function() {

            var window_scroll = $(document).scrollTop();
            var primary_content = $('#primary-content').offset().top;

            if ( window_scroll > primary_content ) {
                $('#back-to-top').addClass('show');
            } else {
                $('#back-to-top').removeClass('show');
            }

        }).scroll();
    }

});

////////////////////////////////////////
// Google Translate Links
////////////////////////////////////////

$('.lang-select').click(function (e) {
    e.preventDefault();
    var lang = $(this).attr('data-lang')
    setLanguage(lang);
});

function setLanguage(theLang) {
    var theSelect = $('.goog-te-combo');
    var db = theSelect.get(0);
    theSelect.val(theLang);
    fireEvent(db, 'change');
}

function fireEvent(element, event) {
    if (document.createEventObject) {
        var evt = document.createEventObject();
        return element.fireEvent('on' + event, evt)
    } else {
        var evt = document.createEvent("HTMLEvents");
        // event type, bubbling, cancelable
        evt.initEvent(event, false, true); 
        return !element.dispatchEvent(evt);
    }
}