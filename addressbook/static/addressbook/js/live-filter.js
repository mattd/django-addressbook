$(document).ready(function() {

	$('#live-filter').submit(function() {
		return false;
	});

	$('#live-filter').keyup(function() {
		clearTimeout($.data(this, "timer"));
		var ms = 200; // milliseconds
		var filterDelayed = setTimeout(function() {
			filterList();
		}, ms);
		$.data(this, "timer", filterDelayed);
		return false;
	});

});

function filterList() {
	$.get(
		window.location.pathname,
		{
			query: $(' [name=q]').val(),
			timestamp: new Date().getTime() 
		},
		function(data) {
			$("#results").html(data);
		}
	)
}
