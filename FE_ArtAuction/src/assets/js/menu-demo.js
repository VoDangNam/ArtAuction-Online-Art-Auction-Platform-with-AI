(function (jQuery) {
    "use strict";
    
    // Menu Toggle Functionality
    jQuery(document).on('click', '.wrapper-menu', function() {
        jQuery(this).toggleClass('open');
    });

    jQuery(document).on('click', ".wrapper-menu", function() {
        jQuery("body").toggleClass("sidebar-main");
    });

    // Initialize tooltips
    jQuery(document).ready(function() {
        jQuery('[data-toggle="tooltip"]').tooltip();
    });

})(jQuery);
