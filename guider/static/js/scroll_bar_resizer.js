console.log('From resizer.js')
// change the default scroll bar of the text area
$('#code').niceScroll({
    background:"rgba(20,20,20,0.3)",
    scrollspeed: 40,
});
// resize the outer scroll bar when the textarea gets resized
jQuery(document).ready(function(){
    var $textareas = jQuery('textarea');

    // store default dimensions
    $textareas.data('x', $textareas.outerWidth());
    $textareas.data('y', $textareas.outerHeight());
    // check for mouseup
    $textareas.mouseup(function(){

        var $this = jQuery(this);
        // check for size change
        if (  $this.outerWidth()  != $this.data('x')
            || $this.outerHeight() != $this.data('y') )
        {
            //resize scrollbar on change
            $("body").getNiceScroll().resize();
        }

        // remember changed dimensions
        $this.data('x', $this.outerWidth());
        $this.data('y', $this.outerHeight());
    });

});