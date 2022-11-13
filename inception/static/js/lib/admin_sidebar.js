$(function() {
    // Add mm-active to the current page's <li>
    var activeUrlName = "/" + $(location).attr('href').split("/").splice(3, 4).join("/");

    $(".inception-link").each(function() {
        if(activeUrlName == $(this).attr('href')){
            $(this).addClass('mm-active');
        }
    });
}); // function
