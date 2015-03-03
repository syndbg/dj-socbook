'use strict';


function activateFormTooltips(fields) {
    fields.forEach(function (field) {
        var $tag = $(field.selector);
        $tag.attr({
            "data-toggle": "tooltip",
            "data-placement": "top",
            "title": field.help_text,
            "trigger": "hover focus"
        });
        $tag.tooltip();
    });
}
