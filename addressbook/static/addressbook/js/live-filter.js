jQuery(document).ready(function() {

	jQuery('#live-filter .submit').hide()

	jQuery('#live-filter').keyup(function() {
		filterList();
		return false;
	});

});

function filterList() {
	jQuery.get(
		window.location.pathname,
		{
			query: jQuery(' [name=q]').val()
		},
		function(data) {
			jQuery("#results").html(data);
		}
	)
}
