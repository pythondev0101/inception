$(document).ready(function(){
    var DELIVERYID;

    $(".btn_details").click(function() {
        DELIVERYID = $(this).closest("tr").children('td:first').text();
        const url = "/bds/api/subscriber/deliveries/" + DELIVERYID;

        $.ajax({
            url: url,
            type: "GET",
            contentType: "application/json; charset=utf-8",
            success: function(data) {
                if (data.id){
                    //body
                    $("#div_details_content").empty();
                    $("#div_details_content").append(
                        `
                        <img src="${data.image_path}" class="img-fluid" alt="Responsive image">
                        `
                    );

                    //details
                    $("#li_subscriber").empty();
                    $("#li_subscriber").append(`<i class="pe-7s-user"> </i>` + "<strong> " + data.subscriber_fname + " " + data.subscriber_lname + "</strong>");
                    $("#li_address").empty();
                    $("#li_address").append(`<i class="pe-7s-map-marker"> </i>` + "<strong> " + data.subscriber_address + "</strong>");
                    $("#li_location").empty();
                    $("#li_location").append(
                        `<i class="pe-7s-map-2"> </i>
                        ` + "<strong>LAT: " + data.latitude + " | LONG: " + data.longitude 
                            +  " | ACC: " + data.accuracy + "</strong>"
                        );
                    $("#li_mobile_date").empty();
                    $("#li_mobile_date").append(`<i class="pe-7s-id"> </i>` + "<strong> " + data.messenger_fname + " " + data.messenger_lname + "</strong>" + "    " +  `<i class="pe-7s-date"> </i>` + "<strong> " + data.date_mobile_delivery + "</strong>");

                    if(data.status == "PENDING"){
                        //footer
                        $("#div_modal_footer").empty();
                        $("#div_modal_footer").append(
                            `
                            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                            <button id="btn_confirm" type="button" class="btn btn-success">Confirm</button>
                            `
                        );

                        //title
                        $("#card_title").empty();
                        $("#card_title").append(
                            `<div class="badge badge-warning">PENDING</div>`
                        );
                    }else if(data.status == "DELIVERED"){
                        //title
                        $("#card_title").empty();
                        $("#card_title").append(
                            `<div class="badge badge-success">DELIVERED</div>`
                        );
                    }
                }

            }
        });
    });


    $("#div_modal_footer").on('click','#btn_confirm',  function(){
        const url = "/bds/api/delivery/" + DELIVERYID + "/confirm";
        var _area_name = $("#btnSubAreaLabel").html()

        $.ajax({
            url: url,
            type: "POST",
            contentType: "application/json; charset=utf-8",
            success: function(data) {
                if (data.result){
                    show_toast('success');
                    $("#btn_confirm").remove();
                    location.reload();
                }else{
                    show_toast('error');
                }
               
            }
        });
    });

    function show_toast(type){
        if (type == "success"){
            $(".toast-success").show();
        }else if (type == "error"){
            $(".toast-error").show();
        }
    }

    function hide_toast(type){
        if (type == "success"){
            $(".toast-success").hide();
        }else if (type == "error"){
            $(".toast-error").hide();
        }
    }

    $(".toast-error").on('click', function(){
        hide_toast('error');
    });

    $(".toast-success").on('click', function(){
        hide_toast('success');
    });


});