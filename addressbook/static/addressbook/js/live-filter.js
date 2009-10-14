jQuery(document).ready(function() {

	jQuery('#live-filter .submit').hide()

	jQuery('#live-filter').submit(function() {
		return false;
	});

	jQuery('#live-filter').keyup(function() {
		clearTimeout(jQuery.data(this, "timer"));
		var ms = 400; // milliseconds
		var wait = setTimeout(function() {
			filterList();
		}, ms);
		jQuery.data(this, "timer", wait);
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
