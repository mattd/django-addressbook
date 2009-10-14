jQuery(document).ready(function() {

	var url = '/addressbook/autocomplete-organization/';

	jQuery("#id_organization").autocomplete(url, {
		autoFill: true,
		max: 50
	});

});
