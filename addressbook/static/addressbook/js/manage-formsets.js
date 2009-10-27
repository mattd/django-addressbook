$(document).ready(function() {

	// For each formset...
	$('.content').find('.model-formset').each(function(i) {

		// Set formset variables.
		var boundForms = $(this).find('.bound');
		var initialUnboundForm = $(this).find('.unbound');
		var theAddLink = $(this).find('a.add');
		var totalFormsInput = $(this).find("input[id$='TOTAL_FORMS']");
		var initialMessage = $(this).find('.initial-message');

		// Configure initial formset display.
		initialUnboundForm.hide();
		if (!boundForms.length) {
			theAddLink.hide();
		} else {
			initialMessage.hide();
		}

		// Make sure TOTAL_FORMS is set correctly.
		var initialTotalForms = boundForms.length + 1;
		totalFormsInput.attr('value',initialTotalForms);

		initialMessage.click(function() {
			$(this).hide();	
			initialUnboundForm.show();
			theAddLink.show();
			return false;
		});

		theAddLink.click(function() {
			var formsContainer = $(this).parent().find('.model-forms');
			var unboundForms = formsContainer.find('.unbound');

			if (unboundForms.attr('style') == 'display: none;') {
				initialUnboundForm.show();
			} else {
				var newForm = initialUnboundForm.clone();
				var newFormInputs = newForm.find("input,textarea,select");
				// Django's formset forms are zero-indexed, so don't increment here.
				var newFormIndex = $(this).parent().find('.model-form').length;

				clearFormFields(newForm);
				prepareForm(newForm);
				newForm.appendTo(formsContainer);
				newFormInputs.each(function(i) {
					var inputId = $(this).attr('id');
					var inputName = $(this).attr('name');
					var re = /\d+/;
					var formIndex = re.exec(inputId);
					$(this).attr({
						'id': inputId.replace(formIndex,newFormIndex), 
						'name': inputName.replace(formIndex,newFormIndex)
					});
				});
				totalFormsInput.val(parseInt(totalFormsInput.val()) + 1);
			}

			return false;
		});

		// For each form within the formset...
		$(this).find('.model-form').each(function(i) {
			prepareForm($(this));
		});

	});

});

function prepareForm(form) {
	 
	// Set form variables.
	var theRemoveLink = form.find('a.remove');
	var deleteSpan = form.find('.delete');
	var formset = form.parents('.model-formset');

	// Configure initial form display.
	deleteSpan.hide();

	// Make sure unbound forms are cleared.
	if (form.hasClass('unbound')) {
		clearFormFields(form);
	} 

	// Setup form behavior.
	theRemoveLink.click(function() {

		form.hide();
		if (form.hasClass('bound')) {
			deleteSpan.find('input').attr('checked','checked');
		} else {
			clearFormFields(form);
		}

		if (form.siblings('.model-form:visible').length == 0) {
			formset.find('.add').hide();
			formset.find('.initial-message').show();			
		}

		return false;
	});

}

function clearFormFields(form) {
	var fields = form.find("input[type='text'],textarea,select");
	$.each(fields, function() {
		if (this.tagName == "select") {
			$(this).find("option:contains(---)").attr("selected", true);
		} else {
			$(this).val("");
		}
	});
}
