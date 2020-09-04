var pkry = $('.packery-container').packery({
  itemSelector: '.home-item',
  gutter: 10,
  isOriginLeft: false,
  // initLayout: false,
});

var searchForm = document.querySelector('#search-form');
searchForm.addEventListener('submit', function(event) {
  event.preventDefault();
  var searchText = "*";
  if (document.querySelector('#search-text') && document.querySelector('#search-text').value.length > 0) {
  	searchText = document.querySelector('#search-text').value;
  }
  
  var term_search_prefix = 'esdsl=%7B%22query%22%3A%7B%22query_string%22%3A%7B%22query%22%3A%22';
  var term_serch_suffix = '%22%7D%7D%7D';
  window.location.href = '/catalog/?'+ term_search_prefix + searchText + term_serch_suffix;
});

$(document).ready(function() {
  var recordCountCallback = function(data) {
    numFound = data.hits.total.value;
    $('#record-count').html(numFound);
  }
  // solr.getRecordCount(recordCountCallback);
  var getRecordCount = function(callback) {
    $.ajax({
      type:"POST",
      url: CATALOG_QUERY_ENDPOINT,
      data:  {"query":{"match_all":{}}},
      success: callback,
      dataType: 'json'
    }).fail(function(){
      $('#record-count').html('');
      console.log('Failed to retrieve number of records from catalog.')
    })
  }
  if (CATALOG_QUERY_ENDPOINT){
    getRecordCount(recordCountCallback);
  }
});
