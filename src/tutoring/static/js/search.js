$(document).on('input', '#search', filter)

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

    let name = info.substring(0, hash).toLowerCase();
    let number = info.substring(hash + 1).toLowerCase();

    return name.indexOf(query) != -1 || number === query;
}

function filter() {
    let query = $('#search').val();

    for(let i = 0; i < cards.length; i++)  {
        $card = $(cards[i]);

        if(matches($card, query)) {
            $card.show();
        } else {
            $card.hide();
        }
    }
}