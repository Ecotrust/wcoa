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
  window.location.href = '/catalog/?text='+searchText;
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
