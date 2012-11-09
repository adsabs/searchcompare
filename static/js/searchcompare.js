
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

// jquery-bbq stuff...
$(window).bind( 'hashchange', function(e) {
    var hashQuery = jQuery.deparam.fragment();
    if (hashQuery.classic || hashQuery.solr) {
        $("#input-classic").val(hashQuery.classic);
        $("#input-solr").val(hashQuery.solr);
        $("#search-button").click();
    }
});
 
$(document).ready(function() {
	$("#search-button").bind('click', function(e) {
		$("ol.resultsList").empty();
		$('div.resultsMeta').empty();
		var classicQuery = $("#input-classic").val();
		var solrQuery = $("#input-solr").val();
		location.href = jQuery.param.fragment( location.href, {classic: classicQuery, solr: solrQuery});
		Sijax.request('search_classic', [$("#input-classic").val()]);
		Sijax.request('search_solr', [$("#input-solr").val()]);
	})
	$(window).trigger( 'hashchange' );
});
