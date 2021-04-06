 $(document).ready(function(){
    $('.datepicker').datepicker();
            format: "dd mmmm, yyyy",
        yearRange: 10,
        showClearBtn: true,
        i18n: {
            done: "Select"
        }
    });