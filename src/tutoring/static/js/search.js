$(document).on('input', '#search', search)
$(document).on('change', '#status-select', status)

let cards = [];

$(document).ready(function () {
    cards = $(".card");
})

function matches(card, query) {
    if(query.length == 0) {
        return true;
    }

    query = query.toLowerCase();
    
    let info = card.find(".card-title").text();
    let hash = info.indexOf("#");
    let open = info.indexOf("(");
    let close = info.indexOf(")");

    let name = info.substring(0, hash).toLowerCase();
    let number = info.substring(hash + 1, open - 1).toLowerCase();
    let status = info.substring(open + 1, close).toLowerCase();

    console.log(name)
    console.log(number === query)
    console.log('"' + status + '"')
    console.log('"' + query + '"')

    return name.indexOf(query) != -1 || number === query || status === query;
}

function filter() {
    let search = $('#search').val();
    let filter = $("#status-select option:selected").text();
    let query = "";

    if(search.length === 0 && filter === "Status")
        return;
    
    if(search.length === 0)
        query = filter;
    else
        query = search;

    console.log(query)

    for(let i = 0; i < cards.length; i++)  {
        $card = $(cards[i]);

        if(matches($card, query)) {
            $card.show();
        } else {
            $card.hide();
        }
    }
}

function search() {
    $('#status-select').val("");
    filter();
}

function status() {
    $('#search').val("");
    filter();
}