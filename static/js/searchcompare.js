
function get_solr_results() {
	
}

function get_classic_results() {
	
}

$(document).ready(function() {
	$("#search-button").bind('click', function(e) {
		Sijax.request('search_classic', [$("#input-classic").val()])
		Sijax.request('search_solr', [$("#input-solr").val()])
	})
});