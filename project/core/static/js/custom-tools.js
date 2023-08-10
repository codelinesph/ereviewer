$(document).ready(function(){
    var ending_input = document.createElement('input');

    ending_input.className = "form-control rounded-0";
    ending_input.id = "ending-input-display"
    $("#ending-date-selector").parent().append(ending_input);


    $('.date-range-picker').daterangepicker({
        minDate: moment(),
        alwaysShowCalendars: true,
        ranges: {
            'Until Tommorow': [moment(), moment().add(1, 'days')],
            'For Next 7 Days': [moment(), moment().add(6, 'days'), moment()],
            'For Next 30 Days': [moment(), moment().add(29, 'days')],
            'This Month': [moment().startOf('month'), moment().endOf('month')],
            'Until End of Next Month': [moment(), moment().add(1, 'month').endOf('month')]
        },
    });
});