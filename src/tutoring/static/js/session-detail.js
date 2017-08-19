function saveNotes() {
    let notes = $('#notes').val();
    let id = $('#sessionId').val();
    let csrfToken = $('input[name="csrfmiddlewaretoken"]').val()

    if(notes) {
        $.post('/session/' + id + '/notes', { notes: notes, csrfmiddlewaretoken: csrfToken });
    }
}

$(document).on('click', '#modifyNotes', saveNotes);