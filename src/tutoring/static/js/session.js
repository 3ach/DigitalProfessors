function updateBilled() {
    let start = $('#id_start_time').val();
    let end = $('#id_end_time').val();
    let date = $('#id_date').val();
    let hourly = $('#id_hourly').val();

    if(start && end && date && hourly) {
        let start_dt = new Date(date + ' ' + start);
        let end_dt = new Date(date + ' ' + end);
        let difference = end_dt - start_dt;
        let hours = difference / (1000 * 60 * 60);
        let billed = hours * hourly;

        if(billed < 30) {
            billed = 30;
        }

        billed = billed.toFixed(2);

        $('#id_billed').val(billed);
    }
}

$(document).on('change', '#id_start_time', updateBilled);
$(document).on('change', '#id_end_time', updateBilled);
$(document).on('change', '#id_date', updateBilled);
$(document).on('change', '#id_hourly', updateBilled);
