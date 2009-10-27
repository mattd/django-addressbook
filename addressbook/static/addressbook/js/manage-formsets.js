$(document).ready(function() {

	// For each formset...
	$('.content').find('.model-formset').each(function(i) {

		// Set formset variables.
		var boundForms = $(this).find('.bound');
		var initialUnboundForm = $(this).find('.unbound');
		var initialMessage = $(this).find('.initial-message');
		var theAddLink = $(this).find('a.add');
		var totalFormsInput = $(this).find("input[id$='TOTAL_FORMS']");

		// Define formset-local functions.
		function toggleActionLinks() {
			initialMessage.toggle();
			theAddLink.toggle();
		}
		 
		// Configure initial formset display.
		theAddLink.hide();
		if (boundForms.length) {
			initialUnboundForm.hide();
			toggleActionLinks();
		} else {
			initialUnboundForm.hide();
			initialMessage.click(function() {
				toggleActionLinks();
				initialUnboundForm.show();
				return false;
			});
		}

		// Make sure TOTAL_FORMS is set correctly.
		var initialTotalForms = boundForms.length + 1;
		totalFormsInput.attr('value',initialTotalForms);

		theAddLink.click(function() {
			var formsContainer = $(this).parent().find('.model-forms');
			var unboundForms = formsContainer.find('.unbound');
			if ((unboundForms.length == 1) && (unboundForms.attr('style') == 'display: none;')) {
				initialUnboundForm.show();
			} else {
				var newForm = formsContainer.find('div:last-child').clone();
				clearFormFields(newForm);
				prepareForm(newForm);
				newForm.addClass('clone');
				newForm.appendTo(formsContainer);
				incrementForm(newForm);
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

	// Configure initial form display.
	deleteSpan.hide();

	// Make sure unbound forms are cleared.
	if (form.hasClass('unbound')) {
		clearFormFields(form);
	} 

	// Setup form behavior.
	theRemoveLink.click(function() {
		var boundForms = form.parent().find('.bound');
		if (!boundForms.length) {
			toggleActionLinks();
		}

		if (form.hasClass('bound')) {
			deleteSpan.find('input').attr('checked','checked');
			form.hide();
		} else if (form.hasClass('clone')) {
			deincrementTotalForms(form.parents('.model-formset'));
			form.remove();
		} else {
			clearFormFields(form);
			form.hide();
		}

		return false;
	});

}

function incrementForm(form) {
	var inputs = form.find("input,textarea,select");
	inputs.each(function(i) {
		var re = /\d+/;
		var inputId = $(this).attr('id');
		var inputName = $(this).attr('name');
		var formNumber = re.exec(inputId);
		var newFormNumber = parseInt(formNumber) + 1;
		var inputId = inputId.replace(formNumber,newFormNumber);
		var inputName = inputName.replace(formNumber,newFormNumber);
		$(this).attr({'id': inputId, 'name': inputName});
	});
	incrementTotalForms(form.parents('.model-formset'));
}

function incrementTotalForms(formset) {
	var totalFormsInput = formset.find("input[id$='TOTAL_FORMS']");
	totalFormsInput.val(parseInt(totalFormsInput.val()) + 1);
}

function deincrementTotalForms(formset) {
	var totalFormsInput = formset.find("input[id$='TOTAL_FORMS']");
	totalFormsInput.val(parseInt(totalFormsInput.val()) - 1);
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
