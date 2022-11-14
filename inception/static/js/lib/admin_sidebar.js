$(function() {
    // Add mm-active to the current page's <li>
    var activeUrlName = "/" + $(location).attr('href').split("/").splice(3, 4).join("/").split('?')[0];

    console.log(activeUrlName);
    $(".inception-link").each(function() {
        console.log($(this).attr('href'));
        if(activeUrlName == $(this).attr('href')){
            $(this).addClass('mm-active');
        }
    });
}); // function
