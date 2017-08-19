function saveNotes() {
    let notes = $('#notes').val();
    let id = $('#sessionId').val();
    let csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

    if(notes) {
        $.post('/session/' + id + '/notes', { notes: notes, csrfmiddlewaretoken: csrfToken });
    }
}

function updateAccounting() {
    let payment = $('#payment').val();
    let id = $('#sessionId').val();
    let csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

    payment = parseFloat(payment).toFixed(2);

    console.log(payment);

    if(payment) {
        $.post('/session/' + id + '/payment', { payment: payment, csrfmiddlewaretoken: csrfToken }, (data, ts, jqxhr) => {
            window.location.reload();
        });
    }
}

$(document).on('click', '#modifyNotes', saveNotes);
$(document).on('click', '#modifyPayment', updateAccounting);