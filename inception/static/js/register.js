$(document).ready(function(){
    toastr.options = {
        "closeButton": true,
        "debug": false,
        "newestOnTop": false,
        "progressBar": false,
        "positionClass": "toast-top-center",
        "preventDuplicates": false,
        "onclick": null,
        "showDuration": "3000",
        "hideDuration": "1000",
        "timeOut": "5000",
        "extendedTimeOut": "1000",
        "showEasing": "swing",
        "hideEasing": "linear",
        "showMethod": "fadeIn",
        "hideMethod": "fadeOut"
        }

    $('#frm_register').submit(function() {
        var password = $("#password").val();
        var confirm_password = $("#confirm_password").val();

        if(password != confirm_password){
            toastr.error("Submit failed","Password do not match!");
            return false;
        }

        return true; // return false to cancel form action
    });
});