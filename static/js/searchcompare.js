
function get_solr_results() {
	
}

function get_classic_results() {
	
}

jQuery.ajaxSetup({
	  beforeSend: function() {
	     $('div.resultsSpinner').show();
	  },
	  complete: function(){
	     $('div.resultsSpinner').hide();
	  },
	  success: function() { console.log("success!"); }
	});

$(document).ready(function() {
	$("#search-button").bind('click', function(e) {
		$("ol.resultsList").empty();
		Sijax.request('search_classic', [$("#input-classic").val()]);
		Sijax.request('search_solr', [$("#input-solr").val()]);
	})
});