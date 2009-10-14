jQuery(document).ready(function() {

	var url = '/addressbook/autocomplete-organization/';

	jQuery("#id_organization").autocomplete(url, {
		matchContains: true,
		max: 50
	});

});
