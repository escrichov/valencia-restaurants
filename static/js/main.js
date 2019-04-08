function clickFilterEvent (event) {
    const filter = $( event.target ).data("filter");

    if ($( event.target ).hasClass('filter-applied')) {
        $( event.target ).removeClass('filter-applied');
        $( ".filter-item" ).each(function() {
            $(this).show();
        });
        return;
    }

    $( ".filter" ).each(function() {
        $(this).removeClass('filter-applied');
    })
    $( event.target ).addClass('filter-applied');

    if (filter === 'all') {
        $( ".filter-item" ).each(function() {
            $(this).show();
        });
        return;
    }

    $( ".filter-item" ).each(function() {
        var item = $(this);
        const filters = item.data("filters");
        var filterExist = false;
        filters.forEach(function(element) {
            if (element === filter){
                filterExist = true;
            }
        });
        if(filterExist){
            item.show();
        } else {
            item.hide();
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
    $( ".filter" ).click(clickFilterEvent);
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
