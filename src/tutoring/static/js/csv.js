function setHeaders(result, file) {
    let headers = result.meta.fields;
    
    headers.forEach((header, index) => {
        $('select').append($('<option>', {value: index + 1, text: header}));
    })

    headers = ['!!EMPTY!!'].concat(headers);

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