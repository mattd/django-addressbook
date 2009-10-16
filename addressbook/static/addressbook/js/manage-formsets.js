jQuery(document).ready(function() {

	// For each formset...
	jQuery('.content').find('.model-formset').each(function(i) {

		// Set formset variables.
		var boundForms = jQuery(this).find('.bound');
		var unboundForms = jQuery(this).find('.unbound');
		var initialMessage = jQuery(this).find('.initial-message');
		var theAddLink = jQuery(this).find('a.add');

		// Define formset-local functions.
		function toggleActionLinks() {
			initialMessage.toggle();
			theAddLink.toggle();
		}
		 
		// Configure initial formset display.
		theAddLink.hide();
		if (boundForms.length) {
			toggleActionLinks();
		} else {
			unboundForms.hide();
			initialMessage.click(function() {
				toggleActionLinks();
				unboundForms.show();
				return false;
			});
		}

		// For each form within the formset...
		jQuery(this).find('.model-form').each(function(i) {

			// Set form variables.
			var theRemoveLink = jQuery(this).find('a.remove');
			var fields = jQuery(this).find("input[type='text'],textarea,select");

			// Configure initial form display.
			jQuery(this).find('.delete').hide();

			// Setup form behavior.
			theRemoveLink.click(function() {
				if (jQuery(this).parent().hasClass('unbound')) {
					clearFormFields(fields);
				}
				if (!boundForms.length) {
					toggleActionLinks();
					jQuery(this).parent().hide();
				}
				return false;
			});

		});

	});

});

function clearFormFields(fields) {
	jQuery.each(fields, function() {
		if (this.tagName == "select") {
			jQuery(this).find("option:contains(---)").attr("selected", true);
		} else {
			jQuery(this).val("");
		}
	});
}
