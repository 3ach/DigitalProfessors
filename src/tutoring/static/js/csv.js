function setHeaders(result, file) {
    let headers = result.meta.fields;
    
    headers.forEach((header, index) => {
        console.log(header);
        $('select').append($('<option>', {value: index, text: header}));
    })

    $('select').prop('disabled', false);
    $('#submit').prop('disabled', false);
    $('#headers').val(JSON.stringify(headers));
}

function loadFile() {
    let file = this.files[0];

    Papa.parse(file, {
        header: true,
        complete: setHeaders
    });
}



$(document).on('change', '#csvFile', loadFile);