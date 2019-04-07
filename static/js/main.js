function clickEvent (event) {
    const filter = $( event.target ).data("filter");
    $( ".filter" ).each(function() {
        $(this).removeClass('filter-applied');
    })
    $( event.target ).addClass('filter-applied');

    if (filter === 'all') {
        $( ".card" ).each(function() {
            $(this).parent().show();
        });
        return;
    }

    $( ".card" ).each(function() {
        var card = $(this);
        const filters = card.data("filters");
        var filterExist = false;
        filters.forEach(function(element) {
            if (element === filter){
                filterExist = true;
            }
        });
        if(filterExist){
            card.parent().show();
        } else {
            card.parent().hide();
        }
    });
}

$( document ).ready(function() {
    $(".showfilters").click(function(event) {
        $(".filters").toggle();
        $(event.target).text(function(i, text){
            return text === "Show Filters" ? "Hide Filters" : "Show Filters";
        });
    });
    $( ".filter" ).click(clickEvent);
    $( ".button-arrow-left" ).click(function(event){
        var nextImage = $(event.target).parent().data('current-image');
        const imageList = $(event.target).parent().data('image-list');
        if (nextImage === 0) {
            nextImage = imageList.length-1;
        } else {
            nextImage = nextImage - 1;
        }
        const image = imageList[nextImage];
        $(event.target).parent().data('current-image', nextImage);
        $(event.target).parent().css("background-image", 'url(' + image + ')');
    });
    $( ".button-arrow-right" ).click(function(event){
        var nextImage = $(event.target).parent().data('current-image');
        const imageList = $(event.target).parent().data('image-list');
        nextImage = (nextImage + 1) % imageList.length;
        const image = imageList[nextImage];
        $(event.target).parent().data('current-image', nextImage);
        $(event.target).parent().css("background-image", 'url(' + image + ')');
    });
});
